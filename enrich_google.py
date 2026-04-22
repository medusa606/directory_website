"""
enrich_google.py — Monthly Google Places enrichment (ratings, reviews, photos).

Uses only:
  - Find Place (free/unlimited) — to look up google_place_id by name+address
  - Place Details (Basic + Contact fields only) — $25/1,000 after free 28,500/month

Fields refreshed:
  - google_place_id     (delta-fill: only if blank)
  - google_rating       (refresh always)
  - google_review_count (refresh always)
  - photo_url           (delta-fill: only if blank)
  - google_maps_url     (delta-fill: only if blank)
  - google_summary      (delta-fill: only if blank)

Checkpoint file: .google_enrich_checkpoint.json
  — stores the last processed index so runs can be resumed after --limit.

Usage:
    python enrich_google.py --file meridian_candidates.csv [--output enriched.csv]
    python enrich_google.py --file meridian_candidates.csv --inplace
    python enrich_google.py --file meridian_candidates.csv --limit 100
    python enrich_google.py --file meridian_candidates.csv --dry-run
"""

import argparse
import json
import logging
import os
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

FIND_PLACE_URL = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"
PLACE_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"

# Fields split across billing tiers:
#   Basic (free with base Place Details): place_id, name, formatted_address,
#          business_status, photos, url, type
#   Contact (1,000 free/month, then $3/1k): opening_hours,
#          formatted_phone_number, international_phone_number, website
#   Atmosphere (1,000 free/month, then $5/1k): rating, user_ratings_total,
#          editorial_summary
# At --limit 1000, stays within free tier.
DETAIL_FIELDS = ",".join([
    # Basic (free)
    "place_id",
    "name",
    "formatted_address",
    "business_status",
    "photos",
    "url",
    "type",
    # Contact (1,000 free/month)
    "opening_hours",
    "formatted_phone_number",
    "international_phone_number",
    "website",
    # Atmosphere (1,000 free/month)
    "rating",
    "user_ratings_total",
    "editorial_summary",
])

# National-coverage chains — skip to save API quota.
# Local multi-site (Nutmeg, Boston Tea Party, Loaf, etc.) are NOT excluded.
NATIONAL_CHAINS_SKIPLIST = {
    # Convenience & Supermarkets
    "Londis", "Spar", "Kwik Save", "Budgens",
    "Tesco", "Tesco Express", "Tesco Metro",
    "Sainsbury's", "Sainsbury's Local",
    "Asda", "Morrisons", "Morrisons Daily", "Waitrose", "Iceland", "Co-op",
    "Aldi", "Lidl", "Marks & Spencer", "M&S Simply Food", "Costco",
    "Ocado", "Poundland", "Home Bargains", "B&M", "The Range",
    # Coffee
    "Starbucks", "Costa Coffee", "Caffè Nero", "Caffe Nero",
    # Fast Food
    "McDonald's", "McDonalds", "Burger King", "KFC",
    "Subway", "Greggs", "Pret a Manger",
    # Casual Dining
    "Nando's", "Nandos", "Pizza Hut", "Domino's", "Dominos",
    "Pizza Express", "Wagamama", "Five Guys",
    "Wetherspoon", "Harvester", "Toby Carvery", "Zizzi", "Prezzo",
    "Cosy Club", "Loungers", "Lounge",
    # Banks
    "Barclays", "Lloyds Bank", "NatWest", "HSBC", "Santander", "Halifax",
    # Pharmacy
    "Boots", "Boots Pharmacy", "Superdrug", "Lloyds Pharmacy", "Holland & Barrett",
    # DIY
    "B&Q", "Homebase", "Wickes", "Screwfix", "Toolstation",
    # Mobile
    "Vodafone", "EE", "EE Store", "O2", "O2 Store", "Three", "Three Store",
    # Hotels
    "Premier Inn", "Travelodge", "Holiday Inn",
    # Fashion & Retail
    "Primark", "Next", "H&M", "Zara", "Sports Direct", "Wilko",
}

CHECKPOINT_FILENAME = ".google_enrich_checkpoint.json"
REQUEST_DELAY = 0.2   # 5 req/s (well below 50 QPS limit)
MAX_RETRIES = 3


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("enrich_google")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


# ---------------------------------------------------------------------------
# API helpers
# ---------------------------------------------------------------------------

def get_api_key() -> str:
    load_dotenv()
    key = os.environ.get("GOOGLE_PLACES_API_KEY", "")
    if not key:
        raise EnvironmentError("GOOGLE_PLACES_API_KEY not found in .env")
    return key


def find_place_id(name: str, address: str, api_key: str, logger: logging.Logger) -> str | None:
    """
    Use Find Place to look up google_place_id by name + address.
    Returns place_id string or None.
    """
    input_text = f"{name} {address}".strip()
    params = {
        "input": input_text,
        "inputtype": "textquery",
        "fields": "place_id",
        "key": api_key,
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(FIND_PLACE_URL, params=params, timeout=10)
            data = resp.json()
            status = data.get("status")
            if status == "OK":
                candidates = data.get("candidates", [])
                if candidates:
                    return candidates[0].get("place_id")
            elif status == "ZERO_RESULTS":
                return None
            elif status == "OVER_QUERY_LIMIT":
                wait = 10 * attempt
                logger.warning(f"Google over query limit, waiting {wait}s …")
                time.sleep(wait)
            else:
                logger.debug(f"Find Place status {status!r} for {name!r}")
                return None
        except requests.RequestException as exc:
            logger.warning(f"Find Place error (attempt {attempt}): {exc}")
            time.sleep(2)

    return None


def get_place_details(place_id: str, api_key: str, logger: logging.Logger) -> dict:
    """
    Fetch Place Details for the given place_id.
    Returns the result dict or {} on failure.
    """
    params = {
        "place_id": place_id,
        "fields": DETAIL_FIELDS,
        "key": api_key,
    }
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(PLACE_DETAILS_URL, params=params, timeout=10)
            data = resp.json()
            status = data.get("status")
            if status == "OK":
                return data.get("result", {})
            elif status == "OVER_QUERY_LIMIT":
                wait = 10 * attempt
                logger.warning(f"Google over query limit, waiting {wait}s …")
                time.sleep(wait)
            else:
                logger.debug(f"Place Details status {status!r} for {place_id!r}")
                return {}
        except requests.RequestException as exc:
            logger.warning(f"Place Details error (attempt {attempt}): {exc}")
            time.sleep(2)

    return {}


# ---------------------------------------------------------------------------
# Checkpoint helpers
# ---------------------------------------------------------------------------

def load_checkpoint(csv_path: str) -> int:
    """Return the last saved row index for this CSV, or 0."""
    cp_path = Path(csv_path).parent / CHECKPOINT_FILENAME
    if cp_path.exists():
        try:
            data = json.loads(cp_path.read_text())
            if data.get("csv_path") == str(csv_path):
                return int(data.get("last_index", 0))
        except (json.JSONDecodeError, KeyError):
            pass
    return 0


def save_checkpoint(csv_path: str, index: int):
    cp_path = Path(csv_path).parent / CHECKPOINT_FILENAME
    cp_path.write_text(json.dumps({"csv_path": str(csv_path), "last_index": index}))


def clear_checkpoint(csv_path: str):
    cp_path = Path(csv_path).parent / CHECKPOINT_FILENAME
    if cp_path.exists():
        cp_path.unlink()


# ---------------------------------------------------------------------------
# Row enrichment
# ---------------------------------------------------------------------------

def _is_blank(val) -> bool:
    return val is None or str(val).strip().lower() in ("", "nan", "none", "null")


def enrich_row(
    row: dict,
    api_key: str,
    logger: logging.Logger,
) -> dict:
    """Enrich a single row with Google data. Returns updated row dict."""
    name = str(row.get("name", "")).strip()
    if not name:
        return row

    # Skip national chains — saves API quota for independents
    if name in NATIONAL_CHAINS_SKIPLIST or row.get("chain_flag") == "chain":
        logger.debug(f"  Skipping chain: {name!r}")
        return row

    address = str(row.get("address", "")).strip()

    # Resolve place_id (delta-fill: use existing if present)
    place_id = str(row.get("google_place_id", "")).strip()
    if _is_blank(place_id):
        place_id = find_place_id(name, address, api_key, logger)
        if place_id:
            row["google_place_id"] = place_id
            logger.debug(f"  {name!r}: found place_id={place_id}")
        else:
            logger.debug(f"  {name!r}: no Google place_id found")
            return row
    else:
        logger.debug(f"  {name!r}: using existing place_id={place_id}")

    time.sleep(REQUEST_DELAY)

    details = get_place_details(place_id, api_key, logger)
    if not details:
        return row

    # Mark permanently/temporarily closed
    biz_status = details.get("business_status", "")
    if biz_status in ("CLOSED_PERMANENTLY", "CLOSED_TEMPORARILY"):
        row["status"] = "closed"
        logger.info(f"  {name!r}: marked closed (Google: {biz_status})")

    # Always refresh rating + review_count
    rating = details.get("rating")
    review_count = details.get("user_ratings_total")
    if rating is not None:
        row["google_rating"] = str(rating)
    if review_count is not None:
        row["google_review_count"] = str(review_count)

    # Delta-fill: address (validate / fill from Google)
    google_addr = details.get("formatted_address", "")
    if google_addr and _is_blank(row.get("address")):
        row["address"] = google_addr

    # Delta-fill: phone
    phone = details.get("formatted_phone_number") or details.get("international_phone_number", "")
    if phone and _is_blank(row.get("phone")):
        row["phone"] = phone

    # Delta-fill: website
    website = details.get("website", "")
    if website and _is_blank(row.get("website")):
        row["website"] = website

    # Delta-fill: opening_hours (weekday_text joined with "; ")
    oh = details.get("opening_hours", {})
    weekday_text = oh.get("weekday_text", [])
    if weekday_text and _is_blank(row.get("opening_hours")):
        row["opening_hours"] = "; ".join(weekday_text)

    # Delta-fill: google_maps_url
    maps_url = details.get("url", "")
    if maps_url and _is_blank(row.get("google_maps_url")):
        row["google_maps_url"] = maps_url

    # Delta-fill: google_photo_reference (raw ref only — never embed API key in stored data)
    if _is_blank(row.get("google_photo_reference")):
        photos = details.get("photos", [])
        if photos:
            ref = photos[0].get("photo_reference", "")
            if ref:
                row["google_photo_reference"] = ref

    # Delta-fill: google_summary
    if _is_blank(row.get("google_summary")):
        summary = details.get("editorial_summary", {}).get("overview", "")
        if summary:
            row["google_summary"] = summary

    logger.info(
        f"  {name!r}: rating={rating} reviews={review_count}"
    )
    return row


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_enrichment(
    csv_path: str,
    output_path: str,
    dry_run: bool,
    limit: int | None,
    resume: bool,
    logger: logging.Logger,
):
    try:
        api_key = get_api_key()
    except EnvironmentError as exc:
        logger.error(str(exc))
        sys.exit(1)

    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    df = df.where(df != "", other=None)
    logger.info(f"Loaded {len(df):,} rows from {csv_path}")

    start_index = 0
    if resume:
        start_index = load_checkpoint(csv_path)
        if start_index:
            logger.info(f"Resuming from checkpoint index {start_index}")

    rows_to_process = df.index[start_index:]
    if limit:
        rows_to_process = rows_to_process[:limit]
        logger.info(f"Processing up to {limit} rows (starting at index {start_index})")

    counters = {"enriched": 0, "skipped_chain": 0, "no_place_id": 0, "errors": 0}

    for i, idx in enumerate(rows_to_process):
        row = df.loc[idx].to_dict()
        name = row.get("name", "?")

        if dry_run:
            is_chain = (name in NATIONAL_CHAINS_SKIPLIST
                        or row.get("chain_flag") == "chain")
            if is_chain:
                logger.info(f"  [DRY RUN] Skip chain: {name!r}")
                counters["skipped_chain"] += 1
            else:
                logger.info(f"  [DRY RUN] Would enrich: {name!r}")
            continue

        try:
            old_place_id = row.get("google_place_id")
            enriched = enrich_row(row, api_key, logger)
            df.loc[idx] = pd.Series(enriched)

            # Count outcomes
            if (enriched.get("name", "") in NATIONAL_CHAINS_SKIPLIST
                    or enriched.get("chain_flag") == "chain"):
                counters["skipped_chain"] += 1
            elif not _is_blank(enriched.get("google_place_id")):
                counters["enriched"] += 1
            else:
                counters["no_place_id"] += 1
        except Exception as exc:
            logger.error(f"  Error enriching {name!r}: {exc}")
            counters["errors"] += 1

        time.sleep(REQUEST_DELAY)

        # Save checkpoint every 50 rows
        if (i + 1) % 50 == 0:
            save_checkpoint(csv_path, start_index + i + 1)
            df.to_csv(output_path, index=False)
            logger.info(f"  Checkpoint saved at row {start_index + i + 1}")

    # ------------------------------------------------------------------
    # Post-enrichment fixups (applied to ALL rows, not just processed)
    # ------------------------------------------------------------------
    if not dry_run:
        city_fixed = 0
        pending_set = 0
        for idx in df.index:
            # city_slug: set "bristol" for all rows where blank
            if _is_blank(df.at[idx, "city_slug"]):
                df.at[idx, "city_slug"] = "bristol"
                city_fixed += 1
            # status: set "pending" for rows still missing address
            if _is_blank(df.at[idx, "address"]):
                current_status = str(df.at[idx, "status"] or "").strip()
                if current_status not in ("closed", "closing"):
                    df.at[idx, "status"] = "pending"
                    pending_set += 1

        df.to_csv(output_path, index=False)
        logger.info(f"Saved enriched CSV: {output_path}")
        clear_checkpoint(csv_path)
        if city_fixed:
            logger.info(f"  city_slug set to 'bristol': {city_fixed:,}")
        if pending_set:
            logger.info(f"  status set to 'pending' (no address): {pending_set:,}")

    logger.info(
        f"\nGoogle enrichment complete\n"
        f"  Enriched (has place_id): {counters['enriched']:>5,}\n"
        f"  Skipped (chain):         {counters['skipped_chain']:>5,}\n"
        f"  No place_id found:       {counters['no_place_id']:>5,}\n"
        f"  Errors:                  {counters['errors']:>5,}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Monthly Google Places enrichment (ratings, photos, place IDs)."
    )
    parser.add_argument("--file", required=True, help="Input CSV path")
    parser.add_argument("--output", help="Output CSV path (default: <input>_google.csv)")
    parser.add_argument("--inplace", action="store_true", help="Overwrite input file")
    parser.add_argument("--dry-run", action="store_true", help="No API calls or file writes")
    parser.add_argument("--limit", type=int, default=None, help="Max rows to process (for monthly capping)")
    parser.add_argument(
        "--no-resume",
        action="store_true",
        help="Ignore checkpoint and start from row 0",
    )
    args = parser.parse_args()

    input_path = Path(args.file)
    if not input_path.exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    if args.inplace:
        output_path = str(input_path)
    elif args.output:
        output_path = args.output
    else:
        output_path = str(input_path.parent / (input_path.stem + "_google.csv"))

    logger = setup_logging()
    run_enrichment(
        csv_path=str(input_path),
        output_path=output_path,
        dry_run=args.dry_run,
        limit=args.limit,
        resume=not args.no_resume,
        logger=logger,
    )


if __name__ == "__main__":
    main()
