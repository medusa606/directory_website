"""
upload_to_supabase.py — Safe CSV-to-Supabase upload with strict no-overwrite semantics.

Rules:
  - Row NOT in DB  → INSERT
  - Row IN DB      → UPDATE only delta_fill_fields where current DB value IS NULL
  - refresh_always_fields (google_rating, google_review_count) → always UPDATE
  - known_non_delta_fields → never touched on existing rows

Dedup key priority: osm_id first, google_place_id fallback.

Usage:
    python upload_to_supabase.py --file <csv> [--dry-run] [--batch-size 500]
"""

import argparse
import json
import logging
import os
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from supabase import create_client

from supabase_schema import get_column_names, check_for_new_columns

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CONFIG_PATH = Path(__file__).parent / "supabase_config.json"
LOG_DIR = Path(__file__).parent


def load_config() -> dict:
    with open(CONFIG_PATH) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Logging setup
# ---------------------------------------------------------------------------

def setup_logging(dry_run: bool) -> logging.Logger:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = "upload_dry_" if dry_run else "upload_"
    log_path = LOG_DIR / f"{prefix}log_{ts}.txt"

    logger = logging.getLogger("upload")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    fh = logging.FileHandler(log_path, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.info(f"Log file: {log_path}")
    return logger


# ---------------------------------------------------------------------------
# Supabase helpers
# ---------------------------------------------------------------------------

def init_client():
    load_dotenv()
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise EnvironmentError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env")
    return create_client(url, key)


def fetch_existing_keys(client, table: str, logger: logging.Logger) -> tuple[dict, dict]:
    """
    Returns two dicts:
      osm_lookup:    { osm_id: db_row_id }
      google_lookup: { google_place_id: db_row_id }
    where db_row_id is the Supabase `id` PK for update targeting.
    """
    logger.info("Fetching existing keys from DB …")
    osm_lookup: dict[str, str] = {}
    google_lookup: dict[str, str] = {}

    page_size = 1000
    offset = 0
    while True:
        resp = (
            client.table(table)
            .select("id,osm_id,google_place_id")
            .range(offset, offset + page_size - 1)
            .execute()
        )
        rows = resp.data or []
        for row in rows:
            row_id = str(row.get("id", ""))
            osm_id = row.get("osm_id") or ""
            gpid = row.get("google_place_id") or ""
            if osm_id:
                osm_lookup[osm_id] = row_id
            if gpid:
                google_lookup[gpid] = row_id
        if len(rows) < page_size:
            break
        offset += page_size

    logger.info(f"  {len(osm_lookup):,} rows with osm_id, "
                f"{len(google_lookup):,} rows with google_place_id")
    return osm_lookup, google_lookup


def fetch_existing_rows_by_ids(
    client, table: str, ids: list[str], logger: logging.Logger
) -> dict[str, dict]:
    """Batch-fetch full rows by Supabase `id`. Returns { id_str: row_dict }."""
    result: dict[str, dict] = {}
    chunk = 200
    for i in range(0, len(ids), chunk):
        batch = ids[i: i + chunk]
        resp = client.table(table).select("*").in_("id", batch).execute()
        for row in resp.data or []:
            result[str(row["id"])] = row
    return result


# ---------------------------------------------------------------------------
# Row processing
# ---------------------------------------------------------------------------

def clean_value(v) -> str | None:
    """Normalise a CSV cell: blank / 'nan' / 'None' → None."""
    if v is None:
        return None
    s = str(v).strip()
    if s.lower() in ("", "nan", "none", "null"):
        return None
    return s


def build_insert_payload(row: dict, db_columns: list[str]) -> dict:
    """Return a dict of non-null CSV values that exist in the DB schema."""
    payload: dict = {}
    for col in db_columns:
        if col == "id":
            continue
        v = clean_value(row.get(col))
        if v is not None:
            payload[col] = v
    return payload


def build_delta_payload(
    csv_row: dict,
    db_row: dict,
    delta_fill_fields: list[str],
    refresh_always_fields: list[str],
) -> dict:
    """
    Return dict of fields to UPDATE:
    - delta_fill_fields: only where DB value is currently NULL / empty
    - refresh_always_fields: always include if CSV has a value
    """
    payload: dict = {}

    for field in delta_fill_fields:
        db_val = db_row.get(field)
        db_is_null = db_val is None or str(db_val).strip() in ("", "nan", "none", "null")
        csv_val = clean_value(csv_row.get(field))
        if db_is_null and csv_val is not None:
            payload[field] = csv_val

    for field in refresh_always_fields:
        csv_val = clean_value(csv_row.get(field))
        if csv_val is not None:
            payload[field] = csv_val

    return payload


# ---------------------------------------------------------------------------
# Upload orchestration
# ---------------------------------------------------------------------------

def run_upload(
    csv_path: str,
    dry_run: bool,
    batch_size: int,
    logger: logging.Logger,
):
    config = load_config()
    table = config["listings_table"]
    delta_fill_fields = config["delta_fill_fields"]
    refresh_always_fields = config["refresh_always_fields"]

    client = init_client()

    # Live schema check
    db_columns = get_column_names()
    check_for_new_columns(db_columns)

    # Load CSV
    logger.info(f"Loading CSV: {csv_path}")
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    df = df.where(df != "", other=None)  # Normalise empty strings to None
    logger.info(f"  {len(df):,} rows loaded")

    # Pre-flight: existing keys
    osm_lookup, google_lookup = fetch_existing_keys(client, table, logger)

    # Partition rows
    to_insert: list[dict] = []
    to_update: list[tuple[str, dict]] = []  # (db_id, csv_row)

    for _, csv_row in df.iterrows():
        csv_row = csv_row.to_dict()
        osm_id = clean_value(csv_row.get("osm_id"))
        gpid = clean_value(csv_row.get("google_place_id"))

        db_id = None
        if osm_id and osm_id in osm_lookup:
            db_id = osm_lookup[osm_id]
        elif gpid and gpid in google_lookup:
            db_id = google_lookup[gpid]

        if db_id is None:
            to_insert.append(csv_row)
        else:
            to_update.append((db_id, csv_row))

    logger.info(f"Rows to INSERT: {len(to_insert):,}")
    logger.info(f"Rows to check for delta UPDATE: {len(to_update):,}")

    # Counters
    stats = {
        "inserted": 0,
        "delta_updated": 0,
        "rating_refreshed": 0,
        "skipped": 0,
        "errors": 0,
    }

    # ----- INSERTs -----
    if to_insert:
        logger.info("Inserting new rows …")
        insert_payloads = [build_insert_payload(r, db_columns) for r in to_insert]
        # Filter out empty payloads
        insert_payloads = [p for p in insert_payloads if p]

        for i in range(0, len(insert_payloads), batch_size):
            batch = insert_payloads[i: i + batch_size]
            if dry_run:
                logger.info(f"  [DRY RUN] Would insert batch {i // batch_size + 1}: {len(batch)} rows")
                stats["inserted"] += len(batch)
            else:
                try:
                    client.table(table).insert(batch).execute()
                    stats["inserted"] += len(batch)
                    logger.info(f"  Inserted batch {i // batch_size + 1}: {len(batch)} rows")
                except Exception as exc:
                    logger.error(f"  INSERT batch error: {exc}")
                    stats["errors"] += len(batch)

    # ----- DELTAs -----
    if to_update:
        logger.info("Fetching existing rows for delta comparison …")
        db_ids = [db_id for db_id, _ in to_update]
        existing_rows = fetch_existing_rows_by_ids(client, table, db_ids, logger)

        for db_id, csv_row in to_update:
            db_row = existing_rows.get(db_id, {})
            delta = build_delta_payload(
                csv_row, db_row, delta_fill_fields, refresh_always_fields
            )

            if not delta:
                stats["skipped"] += 1
                logger.debug(f"  Skipped id={db_id} (nothing to update)")
                continue

            # Track rating refreshes separately for reporting
            has_rating = any(f in delta for f in refresh_always_fields)
            has_delta = any(f in delta for f in delta_fill_fields)

            if dry_run:
                logger.info(f"  [DRY RUN] Would update id={db_id}: fields={list(delta.keys())}")
                if has_delta:
                    stats["delta_updated"] += 1
                if has_rating:
                    stats["rating_refreshed"] += 1
            else:
                try:
                    client.table(table).update(delta).eq("id", db_id).execute()
                    if has_delta:
                        stats["delta_updated"] += 1
                    if has_rating:
                        stats["rating_refreshed"] += 1
                    logger.debug(f"  Updated id={db_id}: {list(delta.keys())}")
                except Exception as exc:
                    logger.error(f"  UPDATE error id={db_id}: {exc}")
                    stats["errors"] += 1

    # ----- Summary -----
    dry_tag = " [DRY RUN]" if dry_run else ""
    logger.info(
        f"\n{'='*50}\n"
        f"Upload complete{dry_tag}\n"
        f"  Inserted:         {stats['inserted']:>6,}\n"
        f"  Delta updated:    {stats['delta_updated']:>6,}\n"
        f"  Rating refreshed: {stats['rating_refreshed']:>6,}\n"
        f"  Skipped:          {stats['skipped']:>6,}\n"
        f"  Errors:           {stats['errors']:>6,}\n"
        f"{'='*50}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Upload a Meridian CSV to Supabase with safe delta-fill semantics."
    )
    parser.add_argument("--file", required=True, help="Path to input CSV file")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen without touching the DB",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=500,
        metavar="N",
        help="Number of rows per INSERT batch (default: 500)",
    )
    args = parser.parse_args()

    if not Path(args.file).exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    logger = setup_logging(args.dry_run)
    run_upload(
        csv_path=args.file,
        dry_run=args.dry_run,
        batch_size=args.batch_size,
        logger=logger,
    )


if __name__ == "__main__":
    main()
