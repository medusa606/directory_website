"""
enrich_fsa.py — Enrich Meridian CSV rows with FSA Food Hygiene Rating Scheme data.

Uses the public FSA Ratings API v2 (no auth required):
  https://api2.ratings.food.gov.uk/

For each row in the food-relevant categories, it:
  1. Calls /Establishments?name=<name>&address=<postcode> API
  2. Fuzzy-matches the returned establishment against name + address
  3. Fills fsa_rating, fsa_hygiene_score, fsa_establishment_id

Output: new CSV with _fsa suffix (or in-place with --inplace).

Usage:
    python enrich_fsa.py --file meridian_candidates.csv [--output enriched.csv]
    python enrich_fsa.py --file meridian_candidates.csv --inplace
    python enrich_fsa.py --file meridian_candidates.csv --dry-run --limit 20
"""

import argparse
import logging
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from rapidfuzz import fuzz

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

FSA_API_BASE = "https://api.ratings.food.gov.uk"
FSA_HEADERS = {"x-api-version": "2"}

# Only enrich rows in these category_key values (food-related)
FOOD_CATEGORIES = {
    "food_produce",
    "restaurants_cafes",
    "drinks_brewing",
}

MIN_FUZZY_SCORE = 72     # Combined name+address similarity threshold
REQUEST_DELAY = 0.25     # Seconds between API calls (FSA is generous, no hard limit)
MAX_RETRIES = 3


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("enrich_fsa")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


# ---------------------------------------------------------------------------
# FSA API helpers
# ---------------------------------------------------------------------------

def fsa_search(name: str, postcode: str, logger: logging.Logger) -> list[dict]:
    """
    Call FSA Establishments search endpoint.
    Returns list of establishment dicts or [] on failure.
    """
    params = {
        "name": name,
        "address": postcode,
        "pageSize": 10,
    }
    url = f"{FSA_API_BASE}/Establishments"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, params=params, headers=FSA_HEADERS, timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                return data.get("establishments", [])
            if resp.status_code == 429:
                wait = 5 * attempt
                logger.warning(f"FSA rate limit, retrying in {wait}s …")
                time.sleep(wait)
            else:
                logger.debug(f"FSA API {resp.status_code} for: {name!r}")
                return []
        except requests.RequestException as exc:
            logger.warning(f"FSA request error (attempt {attempt}): {exc}")
            time.sleep(2)

    return []


def _normalise_for_match(s: str) -> str:
    """Lower-case, strip punctuation for fuzzy matching."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def best_fsa_match(
    name: str,
    address: str,
    candidates: list[dict],
) -> dict | None:
    """
    Fuzzy-match a list of FSA establishments against our name + address.
    Returns the best candidate dict, or None if below threshold.
    """
    name_norm = _normalise_for_match(name)

    # Extract postcode-like token from our address for comparison
    addr_norm = _normalise_for_match(address)

    best_score = 0
    best_candidate = None

    for cand in candidates:
        cand_name = _normalise_for_match(cand.get("BusinessName", ""))
        cand_addr = _normalise_for_match(
            cand.get("AddressLine1", "") + " " + cand.get("PostCode", "")
        )

        name_score = fuzz.token_set_ratio(name_norm, cand_name)
        addr_score = fuzz.partial_ratio(addr_norm, cand_addr)

        # Weighted: name matters more
        combined = 0.65 * name_score + 0.35 * addr_score

        if combined > best_score:
            best_score = combined
            best_candidate = cand

    if best_score >= MIN_FUZZY_SCORE:
        return best_candidate
    return None


def extract_postcode(address: str) -> str:
    """Extract a UK postcode from a full address string for FSA lookup."""
    if not address:
        return ""
    # UK postcode regex
    match = re.search(
        r"\b([A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2})\b",
        address.upper(),
    )
    return match.group(1) if match else ""


# ---------------------------------------------------------------------------
# Main enrichment logic
# ---------------------------------------------------------------------------

def enrich_row(row: dict, logger: logging.Logger) -> dict:
    """Enrich a single CSV row dict. Returns the row with FSA fields populated."""
    # Skip if already enriched
    if row.get("fsa_establishment_id") and str(row["fsa_establishment_id"]).strip() not in (
        "", "nan", "none", "null"
    ):
        return row

    category_key = str(row.get("category_key", "")).strip()
    if category_key not in FOOD_CATEGORIES:
        return row

    name = str(row.get("name", "")).strip()
    address = str(row.get("address", "")).strip()
    if not name:
        return row

    postcode = extract_postcode(address)
    candidates = fsa_search(name, postcode, logger)

    if not candidates:
        logger.debug(f"  No FSA results for: {name!r}")
        return row

    match = best_fsa_match(name, address, candidates)
    if not match:
        logger.debug(f"  No FSA match above threshold for: {name!r}")
        return row

    # FSA rating band: "5 - Very Good", "3 - Generally Satisfactory" etc.
    rating_value = str(match.get("RatingValue", "")).strip()
    # Hygiene score (lower is better; 0=best, 25=needs improvement)
    hygiene_score = match.get("scores", {}).get("Hygiene")
    establishment_id = str(match.get("FHRSID", "")).strip()

    row["fsa_rating"] = rating_value if rating_value else None
    row["fsa_hygiene_score"] = str(hygiene_score) if hygiene_score is not None else None
    row["fsa_establishment_id"] = establishment_id if establishment_id else None

    logger.info(
        f"  Matched {name!r} → rating={rating_value!r} "
        f"hygiene={hygiene_score} id={establishment_id}"
    )
    return row


def run_enrichment(
    csv_path: str,
    output_path: str,
    dry_run: bool,
    limit: int | None,
    logger: logging.Logger,
):
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    df = df.where(df != "", other=None)
    logger.info(f"Loaded {len(df):,} rows from {csv_path}")

    food_mask = df["category_key"].isin(FOOD_CATEGORIES)
    eligible = df[food_mask]
    logger.info(f"  {len(eligible):,} rows in food categories (eligible for FSA enrichment)")

    if limit:
        eligible = eligible.head(limit)
        logger.info(f"  Limiting to first {limit} eligible rows")

    counters = {"enriched": 0, "skipped": 0, "no_match": 0}

    for idx in eligible.index:
        row = df.loc[idx].to_dict()
        original_id = row.get("fsa_establishment_id")

        if dry_run:
            logger.info(f"  [DRY RUN] Would enrich: {row.get('name', '?')!r}")
            time.sleep(REQUEST_DELAY)
            continue

        enriched_row = enrich_row(row, logger)
        df.loc[idx] = pd.Series(enriched_row)

        if enriched_row.get("fsa_establishment_id") and enriched_row["fsa_establishment_id"] != original_id:
            counters["enriched"] += 1
        else:
            counters["no_match"] += 1

        time.sleep(REQUEST_DELAY)

    if not dry_run:
        df.to_csv(output_path, index=False)
        logger.info(f"Saved enriched CSV: {output_path}")

    logger.info(
        f"\nFSA enrichment complete\n"
        f"  Enriched:  {counters['enriched']:>5,}\n"
        f"  No match:  {counters['no_match']:>5,}\n"
        f"  Skipped:   {counters['skipped']:>5,}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Enrich Meridian CSV with FSA Food Hygiene Ratings."
    )
    parser.add_argument("--file", required=True, help="Input CSV path")
    parser.add_argument(
        "--output",
        help="Output CSV path (default: <input>_fsa.csv)",
    )
    parser.add_argument(
        "--inplace",
        action="store_true",
        help="Overwrite the input file",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print what would happen, no API calls or file writes",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Process only the first N eligible rows (testing)",
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
        output_path = str(input_path.parent / (input_path.stem + "_fsa.csv"))

    logger = setup_logging()
    run_enrichment(
        csv_path=str(input_path),
        output_path=output_path,
        dry_run=args.dry_run,
        limit=args.limit,
        logger=logger,
    )


if __name__ == "__main__":
    main()
