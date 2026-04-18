"""
enrich_companies_house.py — Enrich Meridian CSV with Companies House trading status.

Uses the Companies House API (free, requires registration):
  https://developer.company-information.service.gov.uk/

Requires COMPANIES_HOUSE_API_KEY in .env

For each row, it:
  1. Searches Companies House for a company matching the business name
  2. Fuzzy-matches by name
  3. Sets status field to "active" / "dissolved" / "liquidation" based on company status
  4. Optionally fills website if blank (Companies House rarely has this, but it's there)

Output: CSV with _ch suffix (or --inplace / --output).

Usage:
    python enrich_companies_house.py --file meridian_candidates.csv
    python enrich_companies_house.py --file meridian_candidates.csv --inplace
    python enrich_companies_house.py --file meridian_candidates.csv --limit 30 --dry-run
"""

import argparse
import logging
import os
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv
from rapidfuzz import fuzz

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

CH_API_BASE = "https://api.company-information.service.gov.uk"
REQUEST_DELAY = 0.12      # ~8 req/s — well within 600/5min limit
MAX_RETRIES = 3
MIN_FUZZY_SCORE = 75      # Name similarity threshold

# Map CH company status → our status values
CH_STATUS_MAP = {
    "active": "active",
    "active - proposal to strike off": "active",
    "administration": "active",
    "voluntary-arrangement": "active",
    "dissolved": "closed",
    "liquidation": "closed",
    "receivership": "closed",
    "converted-closed": "closed",
    "insolvency-proceedings": "closed",
    "strike-off-action-in-progress": "closing",
    "open": "active",
    "closed": "closed",
}


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("enrich_ch")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


# ---------------------------------------------------------------------------
# Companies House API helpers
# ---------------------------------------------------------------------------

def get_auth() -> tuple[str, str]:
    load_dotenv()
    api_key = os.environ.get("COMPANIES_HOUSE_API_KEY", "")
    if not api_key:
        raise EnvironmentError(
            "COMPANIES_HOUSE_API_KEY not found in .env — "
            "register at https://developer.company-information.service.gov.uk/"
        )
    # CH uses HTTP Basic auth with the API key as username, blank password
    return (api_key, "")


def ch_search(name: str, auth: tuple[str, str], logger: logging.Logger) -> list[dict]:
    """Search Companies House for a company by name. Returns list of company dicts."""
    params = {"q": name, "items_per_page": 5}
    url = f"{CH_API_BASE}/search/companies"

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(url, params=params, auth=auth, timeout=10)
            if resp.status_code == 200:
                return resp.json().get("items", [])
            if resp.status_code == 429:
                wait = 10 * attempt
                logger.warning(f"CH rate limit, waiting {wait}s …")
                time.sleep(wait)
            elif resp.status_code == 401:
                raise EnvironmentError("Companies House API key invalid or missing.")
            else:
                logger.debug(f"CH API {resp.status_code} for: {name!r}")
                return []
        except requests.RequestException as exc:
            logger.warning(f"CH request error (attempt {attempt}): {exc}")
            time.sleep(2)

    return []


def _normalise(s: str) -> str:
    """Lower-case, strip common suffixes and punctuation for fuzzy matching."""
    s = s.lower()
    # Remove common legal suffixes
    s = re.sub(
        r"\b(ltd|limited|plc|llp|llc|inc|incorporated|group|holdings?|uk)\b\.?",
        "",
        s,
    )
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def best_ch_match(
    name: str,
    address: str,
    candidates: list[dict],
) -> dict | None:
    """
    Fuzzy-match CH candidates against our business name.
    Returns the best match, or None if below threshold.
    """
    name_norm = _normalise(name)
    best_score = 0
    best = None

    for c in candidates:
        ch_name = _normalise(c.get("title", ""))
        score = fuzz.token_set_ratio(name_norm, ch_name)

        # Minor boost if address snippet also matches
        ch_addr = (c.get("address_snippet", "") or "").lower()
        if address and any(tok in ch_addr for tok in address.lower().split() if len(tok) > 3):
            score = min(100, score + 5)

        if score > best_score:
            best_score = score
            best = c

    if best_score >= MIN_FUZZY_SCORE:
        return best
    return None


# ---------------------------------------------------------------------------
# Row enrichment
# ---------------------------------------------------------------------------

def _is_blank(val) -> bool:
    return val is None or str(val).strip().lower() in ("", "nan", "none", "null")


def enrich_row(row: dict, auth: tuple[str, str], logger: logging.Logger) -> dict:
    """Enrich a single row. Returns updated row dict."""
    name = str(row.get("name", "")).strip()
    if not name:
        return row

    address = str(row.get("address", "")).strip()
    candidates = ch_search(name, auth, logger)

    if not candidates:
        logger.debug(f"  No CH results for: {name!r}")
        return row

    match = best_ch_match(name, address, candidates)
    if not match:
        logger.debug(f"  No CH match above threshold for: {name!r}")
        return row

    ch_status_raw = (match.get("company_status") or "").lower()
    mapped_status = CH_STATUS_MAP.get(ch_status_raw)

    if mapped_status == "closed":
        row["status"] = "closed"
        logger.info(f"  {name!r}: status → closed (CH: {ch_status_raw!r})")
    elif mapped_status == "closing":
        row["status"] = "closing"
        logger.info(f"  {name!r}: status → closing (CH: {ch_status_raw!r})")
    elif mapped_status == "active" and _is_blank(row.get("status")):
        # Only set active if currently blank — don't overwrite curated status
        row["status"] = "active"

    return row


# ---------------------------------------------------------------------------
# Orchestration
# ---------------------------------------------------------------------------

def run_enrichment(
    csv_path: str,
    output_path: str,
    dry_run: bool,
    limit: int | None,
    logger: logging.Logger,
):
    try:
        auth = get_auth()
    except EnvironmentError as exc:
        logger.error(str(exc))
        sys.exit(1)

    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    df = df.where(df != "", other=None)
    logger.info(f"Loaded {len(df):,} rows from {csv_path}")

    # Only run on rows without a definitive closed/closing status already
    eligible_mask = ~df["status"].isin(["closed", "closing"])
    eligible = df[eligible_mask]
    logger.info(f"  {len(eligible):,} rows eligible for CH status check")

    if limit:
        eligible = eligible.head(limit)
        logger.info(f"  Limiting to first {limit} rows")

    counters = {"active": 0, "closed": 0, "closing": 0, "no_match": 0}

    for idx in eligible.index:
        row = df.loc[idx].to_dict()
        name = row.get("name", "?")

        if dry_run:
            logger.info(f"  [DRY RUN] Would check: {name!r}")
            time.sleep(REQUEST_DELAY)
            continue

        enriched = enrich_row(row, auth, logger)
        df.loc[idx] = pd.Series(enriched)

        s = enriched.get("status", "")
        if s in counters:
            counters[s] += 1
        else:
            counters["no_match"] += 1

        time.sleep(REQUEST_DELAY)

    if not dry_run:
        df.to_csv(output_path, index=False)
        logger.info(f"Saved enriched CSV: {output_path}")

    logger.info(
        f"\nCompanies House enrichment complete\n"
        f"  Active:    {counters['active']:>5,}\n"
        f"  Closed:    {counters['closed']:>5,}\n"
        f"  Closing:   {counters['closing']:>5,}\n"
        f"  No match:  {counters['no_match']:>5,}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Enrich Meridian CSV with Companies House trading status."
    )
    parser.add_argument("--file", required=True, help="Input CSV path")
    parser.add_argument("--output", help="Output CSV path (default: <input>_ch.csv)")
    parser.add_argument("--inplace", action="store_true", help="Overwrite input file")
    parser.add_argument("--dry-run", action="store_true", help="No changes")
    parser.add_argument("--limit", type=int, default=None, help="Process only first N rows")
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
        output_path = str(input_path.parent / (input_path.stem + "_ch.csv"))

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
