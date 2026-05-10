#!/usr/bin/env python3
"""
Upload booking/delivery URL data from listings_with_bookings.csv into the Supabase listings table.

Maps CSV columns to DB columns:
  deliveroo_url          -> delivery_deliveroo
  uber_eats_url          -> delivery_ubereats
  booking_thefork        -> booking_thefork
  booking_firsttable     -> booking_firsttable
  booking_quandoo        -> booking_quandoo
  booking_designmynight  -> booking_designmynight
  booking_resdiary       -> booking_resdiary

Only rows with at least one non-empty value in these columns are processed.
Updates are keyed on the listing `id` (UUID).
Uses the service role key to bypass RLS.
"""

import csv
import os
import sys
import time
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
    sys.exit(1)

CSV_PATH = os.path.join(os.path.dirname(__file__), "listings_with_bookings.csv")

# CSV column -> DB column mapping
COLUMN_MAP = {
    "deliveroo_url":        "delivery_deliveroo",
    "uber_eats_url":        "delivery_ubereats",
    "booking_thefork":      "booking_thefork",
    "booking_firsttable":   "booking_firsttable",
    "booking_quandoo":      "booking_quandoo",
    "booking_designmynight":"booking_designmynight",
    "booking_resdiary":     "booking_resdiary",
}

BATCH_SIZE = 50


def build_updates(csv_path: str) -> list[dict]:
    """Read CSV and return list of update dicts (id + non-empty mapped columns)."""
    updates = []
    skipped_no_id = 0

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_id = row.get("id", "").strip()
            if not row_id:
                skipped_no_id += 1
                continue

            payload: dict = {"id": row_id}
            for csv_col, db_col in COLUMN_MAP.items():
                val = row.get(csv_col, "").strip()
                if val:
                    payload[db_col] = val

            # Only include rows that have at least one booking/delivery value
            if len(payload) > 1:
                updates.append(payload)

    if skipped_no_id:
        print(f"  Skipped {skipped_no_id} rows with missing id")
    return updates


def upload(client: Client, updates: list[dict], dry_run: bool = False) -> None:
    total = len(updates)
    print(f"\n{'DRY RUN — ' if dry_run else ''}Processing {total} rows...")

    success = 0
    errors = 0

    for i, row in enumerate(updates):
        row_id = row["id"]
        payload = {k: v for k, v in row.items() if k != "id"}

        if dry_run:
            print(f"  [dry] id={row_id}  fields={list(payload.keys())}")
            success += 1
            continue

        try:
            client.table("listings").update(payload).eq("id", row_id).execute()
            success += 1
            if success % 50 == 0:
                print(f"  Updated {success}/{total}...")
        except Exception as e:
            print(f"  ERROR updating id={row_id}: {e}")
            errors += 1

        if i % 10 == 9:
            time.sleep(0.05)  # gentle rate limiting every 10 rows

    print(f"\nDone. Success: {success}, Errors: {errors}")


def main():
    dry_run = "--dry-run" in sys.argv

    print(f"Reading {CSV_PATH}...")
    updates = build_updates(CSV_PATH)
    print(f"Found {len(updates)} rows with booking/delivery data to upsert")

    if not updates:
        print("Nothing to do.")
        return

    # Show a brief sample
    print("\nSample (first 3 rows):")
    for row in updates[:3]:
        print(f"  {row}")

    if not dry_run:
        confirm = input("\nProceed with upsert to Supabase? [y/N] ").strip().lower()
        if confirm != "y":
            print("Aborted.")
            return

    client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    upload(client, updates, dry_run=dry_run)


if __name__ == "__main__":
    main()
