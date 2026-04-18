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
PHOTO_URL_TEMPLATE = (
    "https://maps.googleapis.com/maps/api/place/photo"
    "?maxwidth=800&photo_reference={ref}&key={key}"
)

# Minimal fields — avoids Atmosphere (expensive) and is within free tier
DETAIL_FIELDS = ",".join([
    "place_id",
    "name",
    "url",
    "photos",
    "rating",
    "user_ratings_total",
    "business_status",
    "editorial_summary",
])

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
    key = os.environ.get("GOOGLE_MAPS_API_KEY", "")
    if not key:
        raise EnvironmentError("GOOGLE_MAPS_API_KEY not found in .env")
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

    # Skip permanently closed
    if details.get("business_status") in ("CLOSED_PERMANENTLY", "CLOSED_TEMPORARILY"):
        row["status"] = "closed"
        logger.info(f"  {name!r}: marked closed (Google business_status)")

    # Always refresh rating + review_count
    rating = details.get("rating")
    review_count = details.get("user_ratings_total")
    if rating is not None:
        row["google_rating"] = str(rating)
    if review_count is not None:
        row["google_review_count"] = str(review_count)

    # Delta-fill: google_maps_url
    maps_url = details.get("url", "")
    if maps_url and _is_blank(row.get("google_maps_url")):
        row["google_maps_url"] = maps_url

    # Delta-fill: photo_url
    if _is_blank(row.get("photo_url")):
        photos = details.get("photos", [])
        if photos:
            ref = photos[0].get("photo_reference", "")
            if ref:
                row["photo_url"] = PHOTO_URL_TEMPLATE.format(ref=ref, key=api_key)

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

    counters = {"enriched": 0, "no_place_id": 0, "errors": 0}

    for i, idx in enumerate(rows_to_process):
        row = df.loc[idx].to_dict()
        name = row.get("name", "?")

        if dry_run:
            logger.info(f"  [DRY RUN] Would enrich: {name!r}")
            continue

        try:
            enriched = enrich_row(row, api_key, logger)
            df.loc[idx] = pd.Series(enriched)

            if not _is_blank(enriched.get("google_place_id")):
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
            logger.info(f"  Checkpoint saved at row {start_index + i + 1}")

    if not dry_run:
        df.to_csv(output_path, index=False)
        logger.info(f"Saved enriched CSV: {output_path}")
        clear_checkpoint(csv_path)

    logger.info(
        f"\nGoogle enrichment complete\n"
        f"  Enriched (has place_id): {counters['enriched']:>5,}\n"
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
