"""
enrich_wikidata.py — Enrich Meridian CSV rows with Wikidata descriptions and chain detection.

Uses Wikidata SPARQL endpoint (free, no auth):
  https://query.wikidata.org/sparql

For each row, it:
  1. Queries Wikidata for a business entity matching the name (+ optional UK location context)
  2. Fills wikidata_id (e.g. Q12345) and google_summary (English description) if blank
  3. Sets chain_flag=True if the entity is a chain/franchise (subclass of Q507619 or Q17127020)

Output: new CSV with _wikidata suffix (or --inplace / --output).

Usage:
    python enrich_wikidata.py --file meridian_candidates.csv
    python enrich_wikidata.py --file meridian_candidates.csv --inplace
    python enrich_wikidata.py --file meridian_candidates.csv --limit 30
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

SPARQL_ENDPOINT = "https://query.wikidata.org/sparql"
SPARQL_HEADERS = {
    "Accept": "application/sparql-results+json",
    "User-Agent": "MeridianDirectory/1.0 (meridian.directory; enrichment bot)",
}

REQUEST_DELAY = 1.0       # Wikidata asks for ≥1 req/s courtesy
MAX_RETRIES = 3
MIN_LABEL_SCORE = 80      # Fuzzy threshold for name match

# Wikidata QIDs for chain/franchise types
CHAIN_QIDS = {
    "Q507619",    # restaurant chain
    "Q17127020",  # retail chain
    "Q891723",    # public limited company (large)
    "Q4830453",   # business chain
    "Q6881511",   # enterprise (catch-all for big brands)
}


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("enrich_wikidata")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


# ---------------------------------------------------------------------------
# SPARQL helpers
# ---------------------------------------------------------------------------

def sparql_query(query: str, logger: logging.Logger) -> list[dict]:
    """Execute a SPARQL query; return list of result bindings or []."""
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = requests.get(
                SPARQL_ENDPOINT,
                params={"query": query, "format": "json"},
                headers=SPARQL_HEADERS,
                timeout=15,
            )
            if resp.status_code == 200:
                return resp.json().get("results", {}).get("bindings", [])
            if resp.status_code == 429:
                wait = 10 * attempt
                logger.warning(f"Wikidata rate limit, waiting {wait}s …")
                time.sleep(wait)
            elif resp.status_code == 500:
                # Wikidata 500 often means bad query / no results, not a server error
                return []
            else:
                logger.debug(f"Wikidata SPARQL {resp.status_code}")
                return []
        except requests.RequestException as exc:
            logger.warning(f"Wikidata request error (attempt {attempt}): {exc}")
            time.sleep(3)

    return []


def lookup_entity(name: str, logger: logging.Logger) -> list[dict]:
    """
    Search Wikidata for business entities matching the given name.
    Returns a list of candidate dicts with keys: qid, label, description, instance_of_qids.
    """
    # Escape name for SPARQL string literal
    name_escaped = name.replace('"', '\\"').replace("\\", "\\\\")

    query = f"""
SELECT ?item ?itemLabel ?itemDescription ?instanceOf WHERE {{
  ?item wikibase:sitelinks ?sitelinks .
  ?item rdfs:label "{name_escaped}"@en .
  OPTIONAL {{ ?item wdt:P31 ?instanceOf . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
}}
LIMIT 5
"""
    bindings = sparql_query(query, logger)

    results = []
    seen = set()
    for b in bindings:
        qid = b.get("item", {}).get("value", "").split("/")[-1]
        if qid in seen:
            continue
        seen.add(qid)
        instance_qids_raw = b.get("instanceOf", {}).get("value", "")
        instance_qid = instance_qids_raw.split("/")[-1] if instance_qids_raw else ""
        results.append({
            "qid": qid,
            "label": b.get("itemLabel", {}).get("value", ""),
            "description": b.get("itemDescription", {}).get("value", ""),
            "instance_qid": instance_qid,
        })

    # Fallback: use wikibase:mwapi search if exact label match returned nothing
    if not results:
        results = _search_fallback(name_escaped, logger)

    return results


def _search_fallback(name_escaped: str, logger: logging.Logger) -> list[dict]:
    """MediaWiki API fulltext search as fallback for name lookup."""
    query = f"""
SELECT ?item ?itemLabel ?itemDescription ?instanceOf WHERE {{
  SERVICE wikibase:mwapi {{
    bd:serviceParam wikibase:api "EntitySearch" ;
                    wikibase:endpoint "www.wikidata.org" ;
                    mwapi:search "{name_escaped}" ;
                    mwapi:language "en" ;
                    mwapi:limit "5" .
    ?item wikibase:apiOutputItem mwapi:item .
  }}
  OPTIONAL {{ ?item wdt:P31 ?instanceOf . }}
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" . }}
}}
LIMIT 5
"""
    bindings = sparql_query(query, logger)

    results = []
    seen = set()
    for b in bindings:
        qid = b.get("item", {}).get("value", "").split("/")[-1]
        if qid in seen:
            continue
        seen.add(qid)
        instance_qids_raw = b.get("instanceOf", {}).get("value", "")
        instance_qid = instance_qids_raw.split("/")[-1] if instance_qids_raw else ""
        results.append({
            "qid": qid,
            "label": b.get("itemLabel", {}).get("value", ""),
            "description": b.get("itemDescription", {}).get("value", ""),
            "instance_qid": instance_qid,
        })
    return results


def is_chain_entity(candidates: list[dict]) -> bool:
    """Return True if any candidate's instance_qid indicates a chain/franchise."""
    for c in candidates:
        if c.get("instance_qid") in CHAIN_QIDS:
            return True
    return False


def best_match(name: str, candidates: list[dict]) -> dict | None:
    """Return the candidate with the highest label similarity, or None if below threshold."""
    if not candidates:
        return None

    name_norm = name.lower().strip()
    best_score = 0
    best = None

    for c in candidates:
        score = fuzz.token_set_ratio(name_norm, c.get("label", "").lower())
        if score > best_score:
            best_score = score
            best = c

    if best_score >= MIN_LABEL_SCORE:
        return best
    return None


# ---------------------------------------------------------------------------
# Row enrichment
# ---------------------------------------------------------------------------

def _is_blank(val) -> bool:
    return val is None or str(val).strip().lower() in ("", "nan", "none", "null")


def enrich_row(row: dict, logger: logging.Logger) -> dict:
    """Enrich a single row with Wikidata data. Returns updated row."""
    # Skip if already has wikidata_id
    if not _is_blank(row.get("wikidata_id")):
        return row

    name = str(row.get("name", "")).strip()
    if not name:
        return row

    candidates = lookup_entity(name, logger)

    if not candidates:
        logger.debug(f"  No Wikidata results for: {name!r}")
        return row

    # Check chain flag regardless of best match
    if is_chain_entity(candidates):
        row["chain_flag"] = "true"
        logger.info(f"  {name!r}: chain flag set (Wikidata instance match)")

    match = best_match(name, candidates)
    if not match:
        logger.debug(f"  No Wikidata match above threshold for: {name!r}")
        return row

    row["wikidata_id"] = match["qid"]

    # Fill description if google_summary is blank
    desc = match.get("description", "").strip()
    if desc and _is_blank(row.get("google_summary")):
        # Capitalise first letter
        row["google_summary"] = desc[0].upper() + desc[1:] if desc else desc
        logger.info(f"  {name!r}: Wikidata description filled: {desc[:60]!r}")

    logger.info(f"  {name!r}: wikidata_id={match['qid']}")
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
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    df = df.where(df != "", other=None)
    logger.info(f"Loaded {len(df):,} rows from {csv_path}")

    # Only enrich rows without wikidata_id
    needs_enrich = df[df["wikidata_id"].isna() | (df["wikidata_id"] == "")]
    logger.info(f"  {len(needs_enrich):,} rows need Wikidata enrichment")

    if limit:
        needs_enrich = needs_enrich.head(limit)
        logger.info(f"  Limiting to first {limit} rows")

    counters = {"enriched": 0, "chain_flagged": 0, "no_match": 0}

    for idx in needs_enrich.index:
        row = df.loc[idx].to_dict()
        name = row.get("name", "?")

        if dry_run:
            logger.info(f"  [DRY RUN] Would enrich: {name!r}")
            time.sleep(REQUEST_DELAY)
            continue

        enriched = enrich_row(row, logger)
        df.loc[idx] = pd.Series(enriched)

        if not _is_blank(enriched.get("wikidata_id")):
            counters["enriched"] += 1
        else:
            counters["no_match"] += 1

        if str(enriched.get("chain_flag", "")).lower() == "true":
            counters["chain_flagged"] += 1

        time.sleep(REQUEST_DELAY)

    if not dry_run:
        df.to_csv(output_path, index=False)
        logger.info(f"Saved enriched CSV: {output_path}")

    logger.info(
        f"\nWikidata enrichment complete\n"
        f"  Wikidata ID found: {counters['enriched']:>5,}\n"
        f"  Chain flagged:     {counters['chain_flagged']:>5,}\n"
        f"  No match:          {counters['no_match']:>5,}"
    )


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Enrich Meridian CSV with Wikidata descriptions and chain detection."
    )
    parser.add_argument("--file", required=True, help="Input CSV path")
    parser.add_argument("--output", help="Output CSV path (default: <input>_wikidata.csv)")
    parser.add_argument("--inplace", action="store_true", help="Overwrite input file")
    parser.add_argument("--dry-run", action="store_true", help="No changes, print what would happen")
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
        output_path = str(input_path.parent / (input_path.stem + "_wikidata.csv"))

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
