"""
generate_slugs.py — Generate city_slug and area_slug for Meridian CSV rows.

Uses lat/lon coordinates to find the nearest Bristol neighbourhood via
precomputed centroids. Fetches centroids from Nominatim on first run and
caches them to bristol_neighbourhoods.json.

Rules:
  - city_slug: derived from postcode prefix (BS* → bristol)
  - area_slug: nearest neighbourhood centroid by haversine distance
  - Existing non-empty slugs are preserved (never overwritten)
  - Rows with no address AND no website → status set to "unverified"

Usage:
    python generate_slugs.py --file baseline.csv --inplace
    python generate_slugs.py --file baseline.csv --output enriched.csv
    python generate_slugs.py --file baseline.csv --dry-run
    python generate_slugs.py --fetch-centroids          # refresh cached centroids
"""

import argparse
import json
import logging
import math
import re
import sys
import time
from pathlib import Path

import pandas as pd
import requests

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
NOMINATIM_HEADERS = {
    "User-Agent": "MeridianDirectory/1.0 (meridian.directory; slug generator)",
}
NOMINATIM_DELAY = 1.1  # Nominatim requires ≤1 req/s

CACHE_PATH = Path(__file__).parent / "bristol_neighbourhoods.json"

# Postcode prefix → city_slug mapping (extend for new cities)
POSTCODE_CITY_MAP = {
    "BS": "bristol",
}

# Bristol neighbourhoods (within the city boundary, excluding SG/NS/BANES)
BRISTOL_NEIGHBOURHOODS = [
    "Bristol city centre",
    "Arnos Vale",
    "Ashley Down",
    "Ashton Gate",
    "Ashton Vale",
    "Avonmouth",
    "Baptist Mills",
    "Barton Hill",
    "Bedminster",
    "Bedminster Down",
    "Begbrook",
    "Bishopston",
    "Bishopsworth",
    "Blaise Hamlet",
    "Bower Ashton",
    "Brandon Hill",
    "Brentry",
    "Brislington",
    "Broadmead",
    "Broomhill",
    "Chester Park",
    "Clifton",
    "Coombe Dingle",
    "Cotham",
    "Crew's Hole",
    "Crofts End",
    "Easton",
    "Eastville",
    "Filwood Park",
    "Fishponds",
    "Golden Hill",
    "Greenbank",
    "Hartcliffe",
    "Headley Park",
    "Henbury",
    "Hengrove",
    "Henleaze",
    "Hillfields",
    "Horfield",
    "Hotwells",
    "Kensington Park",
    "Kingsdown",
    "Knowle",
    "Knowle West",
    "Lawrence Hill",
    "Lawrence Weston",
    "Lockleaze",
    "Lodge Hill",
    "Mayfield Park",
    "Monks Park",
    "Montpelier",
    "Netham",
    "Oldland Common",
    "Redcliffe",
    "Redfield",
    "Redland",
    "Sea Mills",
    "Shirehampton",
    "Sneyd Park",
    "Southmead",
    "Southville",
    "Speedwell",
    "Spike Island",
    "St Agnes",
    "St Andrews",
    "St Anne's",
    "St George",
    "St Paul's",
    "St Philip's Marsh",
    "St Werburghs",
    "Stapleton",
    "Stockwood",
    "Stoke Bishop",
    "Stokes Croft",
    "Temple Meads",
    "Totterdown",
    "Two Mile Hill",
    "Upper Knowle",
    "Victoria Park",
    "Westbury-on-Trym",
    "Westbury Park",
    "Whitchurch",
    "Whitehall",
    "Windmill Hill",
    "Withywood",
]


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def slugify(text: str) -> str:
    """Convert text to URL-friendly slug (matches scrape_osm.py)."""
    if not text:
        return ""
    text = text.replace("'", "").replace('"', "")
    text = re.sub(r"[\s&/]+", "-", text.lower())
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Return distance in metres between two lat/lon points."""
    R = 6_371_000  # Earth radius in metres
    phi1, phi2 = math.radians(lat1), math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlam = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(dlam / 2) ** 2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def extract_postcode_prefix(address: str) -> str | None:
    """Extract the letter prefix from a UK postcode in an address string."""
    if not address:
        return None
    m = re.search(r"\b([A-Z]{1,2})\d{1,2}[A-Z]?\s*\d[A-Z]{2}\b", address.upper())
    return m.group(1) if m else None


def is_empty(val) -> bool:
    """Check if a value is effectively empty."""
    if val is None:
        return True
    s = str(val).strip()
    return s.lower() in ("", "nan", "none", "null")


# ---------------------------------------------------------------------------
# Centroid fetching & caching
# ---------------------------------------------------------------------------

def fetch_centroids(logger: logging.Logger) -> dict[str, dict]:
    """Fetch lat/lon centroids for all Bristol neighbourhoods from Nominatim.

    Returns dict: { "neighbourhood-slug": {"name": "...", "lat": ..., "lon": ...} }
    """
    centroids = {}
    total = len(BRISTOL_NEIGHBOURHOODS)

    for i, name in enumerate(BRISTOL_NEIGHBOURHOODS, 1):
        slug = slugify(name)
        logger.info(f"  [{i}/{total}] Fetching centroid for '{name}' …")

        try:
            resp = requests.get(
                NOMINATIM_URL,
                params={
                    "q": f"{name}, Bristol, UK",
                    "format": "json",
                    "limit": 1,
                    "addressdetails": 0,
                },
                headers=NOMINATIM_HEADERS,
                timeout=10,
            )
            resp.raise_for_status()
            results = resp.json()

            if results:
                centroids[slug] = {
                    "name": name,
                    "lat": float(results[0]["lat"]),
                    "lon": float(results[0]["lon"]),
                }
                logger.info(f"    → {centroids[slug]['lat']:.5f}, {centroids[slug]['lon']:.5f}")
            else:
                logger.warning(f"    → No result for '{name}'")

        except requests.RequestException as e:
            logger.warning(f"    → Error fetching '{name}': {e}")

        time.sleep(NOMINATIM_DELAY)

    return centroids


def load_or_fetch_centroids(logger: logging.Logger, force_fetch: bool = False) -> dict:
    """Load cached centroids or fetch from Nominatim if missing."""
    if CACHE_PATH.exists() and not force_fetch:
        with open(CACHE_PATH) as f:
            centroids = json.load(f)
        logger.info(f"Loaded {len(centroids)} cached neighbourhood centroids from {CACHE_PATH}")
        return centroids

    logger.info("Fetching neighbourhood centroids from Nominatim …")
    centroids = fetch_centroids(logger)

    if centroids:
        with open(CACHE_PATH, "w") as f:
            json.dump(centroids, f, indent=2)
        logger.info(f"Cached {len(centroids)} centroids to {CACHE_PATH}")

    return centroids


# ---------------------------------------------------------------------------
# Nearest-neighbour lookup
# ---------------------------------------------------------------------------

def find_nearest_neighbourhood(
    lat: float, lon: float, centroids: dict, max_distance_m: float = 3000
) -> str:
    """Find the nearest neighbourhood centroid within max_distance_m.

    Returns the neighbourhood slug, or empty string if none within range.
    """
    best_slug = ""
    best_dist = float("inf")

    for slug, data in centroids.items():
        dist = haversine(lat, lon, data["lat"], data["lon"])
        if dist < best_dist:
            best_dist = dist
            best_slug = slug

    # Only assign if within reasonable distance (default 3km)
    if best_dist <= max_distance_m:
        return best_slug
    return ""


# ---------------------------------------------------------------------------
# City slug from postcode
# ---------------------------------------------------------------------------

def city_slug_from_address(address: str) -> str:
    """Extract city slug from postcode prefix in address."""
    prefix = extract_postcode_prefix(address)
    if prefix:
        return POSTCODE_CITY_MAP.get(prefix, "")
    return ""


# ---------------------------------------------------------------------------
# Main enrichment
# ---------------------------------------------------------------------------

def generate_slugs(
    csv_path: str,
    output_path: str | None,
    inplace: bool,
    dry_run: bool,
    max_distance: float,
    logger: logging.Logger,
):
    centroids = load_or_fetch_centroids(logger)
    if not centroids:
        logger.error("No neighbourhood centroids available. Run with --fetch-centroids first.")
        sys.exit(1)

    # Load CSV
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)
    logger.info(f"Loaded {len(df):,} rows from {csv_path}")

    stats = {
        "city_slug_set": 0,
        "area_slug_set": 0,
        "city_slug_kept": 0,
        "area_slug_kept": 0,
        "status_unverified": 0,
        "no_coords": 0,
    }

    for idx, row in df.iterrows():
        address = str(row.get("address", "")).strip()
        website = str(row.get("website", "")).strip()
        lat_str = str(row.get("latitude", "")).strip()
        lon_str = str(row.get("longitude", "")).strip()

        # --- city_slug ---
        current_city = str(row.get("city_slug", "")).strip()
        if is_empty(current_city):
            new_city = city_slug_from_address(address)
            if new_city:
                df.at[idx, "city_slug"] = new_city
                stats["city_slug_set"] += 1
        else:
            stats["city_slug_kept"] += 1

        # --- area_slug ---
        current_area = str(row.get("area_slug", "")).strip()
        if is_empty(current_area):
            if lat_str and lon_str and lat_str not in ("", "nan") and lon_str not in ("", "nan"):
                try:
                    lat = float(lat_str)
                    lon = float(lon_str)
                    nearest = find_nearest_neighbourhood(lat, lon, centroids, max_distance)
                    if nearest:
                        df.at[idx, "area_slug"] = nearest
                        stats["area_slug_set"] += 1
                except ValueError:
                    stats["no_coords"] += 1
            else:
                stats["no_coords"] += 1
        else:
            stats["area_slug_kept"] += 1

        # --- status: unverified if no address AND no website ---
        if is_empty(address) and is_empty(website):
            current_status = str(row.get("status", "")).strip()
            if current_status not in ("closed", "closing"):
                df.at[idx, "status"] = "unverified"
                stats["status_unverified"] += 1

    # Summary
    logger.info(
        f"\n{'='*50}\n"
        f"Slug generation complete\n"
        f"  city_slug set:       {stats['city_slug_set']:>6,}\n"
        f"  city_slug preserved: {stats['city_slug_kept']:>6,}\n"
        f"  area_slug set:       {stats['area_slug_set']:>6,}\n"
        f"  area_slug preserved: {stats['area_slug_kept']:>6,}\n"
        f"  status → unverified: {stats['status_unverified']:>6,}\n"
        f"  no coordinates:      {stats['no_coords']:>6,}\n"
        f"{'='*50}"
    )

    if dry_run:
        logger.info("[DRY RUN] No file written.")
        return

    # Write output
    if inplace:
        out = csv_path
    elif output_path:
        out = output_path
    else:
        p = Path(csv_path)
        out = str(p.with_name(p.stem + "_slugs" + p.suffix))

    df.to_csv(out, index=False)
    logger.info(f"Saved to {out}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def setup_logging() -> logging.Logger:
    logger = logging.getLogger("slugs")
    logger.setLevel(logging.DEBUG)
    fmt = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)
    return logger


def main():
    parser = argparse.ArgumentParser(
        description="Generate city_slug and area_slug for Meridian CSV rows."
    )
    parser.add_argument("--file", help="Path to input CSV file")
    parser.add_argument("--output", help="Path to output CSV (default: <input>_slugs.csv)")
    parser.add_argument("--inplace", action="store_true", help="Overwrite input file")
    parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    parser.add_argument(
        "--fetch-centroids",
        action="store_true",
        help="Fetch/refresh neighbourhood centroids from Nominatim and exit",
    )
    parser.add_argument(
        "--max-distance",
        type=float,
        default=3000,
        metavar="M",
        help="Maximum distance in metres to match a neighbourhood (default: 3000)",
    )
    args = parser.parse_args()

    logger = setup_logging()

    if args.fetch_centroids:
        load_or_fetch_centroids(logger, force_fetch=True)
        return

    if not args.file:
        parser.error("--file is required (unless using --fetch-centroids)")

    if not Path(args.file).exists():
        print(f"Error: file not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    generate_slugs(
        csv_path=args.file,
        output_path=args.output,
        inplace=args.inplace,
        dry_run=args.dry_run,
        max_distance=args.max_distance,
        logger=logger,
    )


if __name__ == "__main__":
    main()
