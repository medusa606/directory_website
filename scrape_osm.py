"""
scrape_osm.py — Meridian Directory
=====================================
Primary business discovery script using the free Overpass API (OpenStreetMap).

Fetches all relevant businesses within a named OSM administrative area and
produces a schema-aligned CSV ready for enrichment and upload.

USAGE
=====
    # Scrape all categories for City of Bristol
    python scrape_osm.py --area "City of Bristol"

    # Specific categories only
    python scrape_osm.py --area "City of Bristol" --categories food_produce,restaurants_cafes

    # Dry run: print counts and sample, no CSV written
    python scrape_osm.py --area "City of Bristol" --dry-run

    # Scale to any UK area
    python scrape_osm.py --area "Greater Manchester"
    python scrape_osm.py --area "United Kingdom" --timeout 900

COST
====
    Free. No API key required. Overpass API fair-use: <10,000 queries/day, <1GB/day.
    A full Bristol query is typically ~1 request, ~5-15MB, ~30 seconds.
"""

import os
import re
import sys
import csv
import json
import time
import logging
import argparse
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────────
# KNOWN RETAIL CHAINS
# ─────────────────────────────────────────────
KNOWN_CHAINS = {
    "Iceland", "Tesco", "Sainsbury's", "Asda", "Morrisons", "Waitrose",
    "M&S Food Hall", "Marks & Spencer", "Budgens", "Co-op", "Lidl", "Aldi",
    "Ocado", "Poundland", "Home Bargains", "B&M", "The Range",
    "McDonald's", "Burger King", "KFC", "Subway", "Pizza Hut", "Domino's",
    "Costa Coffee", "Starbucks", "Caffè Nero", "Greggs", "Pret a Manger",
    "Boots", "Superdrug", "Holland & Barrett",
    "Wetherspoon", "Harvester", "Toby Carvery",
}

# ─────────────────────────────────────────────
# MERIDIAN CATEGORIES → OSM TAGS
# ─────────────────────────────────────────────
MERIDIAN_CATEGORIES = {
    "food_produce": {
        "label": "Food & Produce",
        "slug": "food-and-produce",
        "osm_filters": [
            {"key": "shop",   "values": ["bakery", "butcher", "greengrocer", "deli", "fishmonger",
                                          "cheese", "confectionery", "chocolate", "supermarket",
                                          "convenience", "farm", "organic", "spices", "seafood"]},
            {"key": "amenity", "values": ["marketplace", "food_court"]},
        ],
    },
    "restaurants_cafes": {
        "label": "Restaurants & Cafés",
        "slug": "restaurants-and-cafes",
        "osm_filters": [
            {"key": "amenity", "values": ["restaurant", "cafe", "fast_food", "food_court", "ice_cream"]},
        ],
    },
    "drinks_brewing": {
        "label": "Drinks & Brewing",
        "slug": "drinks-and-brewing",
        "osm_filters": [
            {"key": "amenity", "values": ["bar", "pub", "biergarten"]},
            {"key": "craft",   "values": ["brewery", "distillery", "winery", "cidery", "meadery"]},
            {"key": "shop",    "values": ["wine", "alcohol", "beer", "beverages"]},
        ],
    },
    "craft_makers": {
        "label": "Craft & Makers",
        "slug": "craft-and-makers",
        "osm_filters": [
            {"key": "craft", "values": ["ceramics", "jeweller", "jewellery", "blacksmith", "weaver",
                                         "glassblower", "bookbinder", "leather", "tailor", "cobbler",
                                         "printer", "woodworker", "carpenter", "goldsmith", "silversmith",
                                         "clockmaker", "gunsmith", "knifemaker", "furniture"]},
            {"key": "shop",  "values": ["jewelry", "art", "craft", "maker"]},
        ],
    },
    "art_design": {
        "label": "Art & Design",
        "slug": "art-and-design",
        "osm_filters": [
            {"key": "amenity", "values": ["arts_centre", "art_gallery"]},
            {"key": "shop",    "values": ["art", "photo", "frame", "design"]},
            {"key": "craft",   "values": ["photographer", "sculptor", "illustrator", "artist",
                                           "graphic_designer", "muralist", "printmaker"]},
        ],
    },
    "home_interiors": {
        "label": "Home & Interiors",
        "slug": "home-and-interiors",
        "osm_filters": [
            {"key": "shop", "values": ["furniture", "antiques", "interior_decoration",
                                        "second_hand", "vintage", "curtain", "carpet",
                                        "lighting", "paint", "tiles", "homeware"]},
        ],
    },
    "plants_garden": {
        "label": "Plants & Garden",
        "slug": "plants-and-garden",
        "osm_filters": [
            {"key": "shop",    "values": ["florist", "garden_centre", "garden_center",
                                           "seeds", "plants", "horticulture"]},
            {"key": "craft",   "values": ["gardener", "landscape_architect"]},
            {"key": "amenity", "values": ["community_garden"]},
        ],
    },
    "health_wellbeing": {
        "label": "Health & Wellbeing",
        "slug": "health-and-wellbeing",
        "osm_filters": [
            {"key": "amenity",     "values": ["spa", "massage", "sauna"]},
            {"key": "leisure",     "values": ["fitness_centre", "sports_centre", "yoga", "dance"]},
            {"key": "healthcare",  "values": ["alternative", "therapist", "herbalist",
                                               "acupuncture", "naturopath", "osteopath",
                                               "physiotherapist", "audiologist"]},
            {"key": "shop",        "values": ["nutrition_supplements", "herbalist", "massage",
                                               "wellness", "beauty", "hairdresser"]},
        ],
    },
}

OVERPASS_ENDPOINT = "https://overpass-api.de/api/interpreter"


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def slugify(text: str) -> str:
    if not text:
        return ""
    text = text.replace("'", "").replace('"', "")
    text = re.sub(r"[\s&/]+", "-", text.lower())
    text = re.sub(r"[^a-z0-9-]", "", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def is_chain(name: str) -> bool:
    name_upper = name.upper()
    return any(c.upper() in name_upper for c in KNOWN_CHAINS)


def extract_city_area_from_tags(tags: dict) -> tuple[str, str]:
    """Best-effort extraction of city and area slugs from OSM addr:* tags."""
    city_raw = (
        tags.get("addr:city")
        or tags.get("addr:town")
        or tags.get("addr:county")
        or ""
    )
    area_raw = (
        tags.get("addr:suburb")
        or tags.get("addr:neighbourhood")
        or tags.get("addr:quarter")
        or tags.get("addr:district")
        or ""
    )
    return slugify(city_raw), slugify(area_raw)


def build_address(tags: dict) -> str:
    """Reconstruct a formatted address string from OSM addr:* tags."""
    parts = []
    for k in ["addr:housenumber", "addr:housename", "addr:street",
              "addr:postcode", "addr:city", "addr:country"]:
        v = tags.get(k, "").strip()
        if v:
            if k in ("addr:housenumber", "addr:housename", "addr:street"):
                parts.append(v)
            else:
                parts.append(v)
    if not parts:
        return ""
    # housenumber + street join without comma, then city and postcode with commas
    addr_line = " ".join(filter(None, [
        tags.get("addr:housenumber", "").strip() or tags.get("addr:housename", "").strip(),
        tags.get("addr:street", "").strip(),
    ]))
    postcode = tags.get("addr:postcode", "").strip()
    city     = tags.get("addr:city", "").strip() or tags.get("addr:town", "").strip()
    country  = tags.get("addr:country", "").strip()
    pieces = [p for p in [addr_line, city, postcode, country] if p]
    return ", ".join(pieces)


def aggregate_tags(tags: dict) -> str:
    """Build a PostgreSQL-style text array from relevant OSM type keys."""
    values = []
    for key in ("amenity", "shop", "craft", "leisure", "healthcare", "cuisine", "tourism"):
        v = tags.get(key)
        if v:
            values.extend(v.split(";"))  # OSM uses semicolons for multiple values
    cleaned = [v.strip() for v in values if v.strip()]
    if not cleaned:
        return ""
    return "{" + ",".join(f'"{v}"' for v in cleaned) + "}"


def get_lat_lon(element: dict) -> tuple[float | None, float | None]:
    """Extract lat/lon from a node or from a way/relation center."""
    if element.get("type") == "node":
        return element.get("lat"), element.get("lon")
    center = element.get("center", {})
    return center.get("lat"), center.get("lon")


# ─────────────────────────────────────────────
# OVERPASS QUERY BUILDER
# ─────────────────────────────────────────────

def build_overpass_query(area_name: str, category_key: str, timeout: int = 180) -> str:
    """Build an Overpass QL query for a single Meridian category within a named area.

    Uses an OSM area boundary lookup so results are restricted exactly to the
    administrative area — this eliminates the radius-outlier problem present in
    Google Nearby Search.
    """
    cat = MERIDIAN_CATEGORIES[category_key]
    filters = cat["osm_filters"]

    # Build union of nwr[] statements for each filter
    union_parts = []
    for f in filters:
        key = f["key"]
        values = f["values"]
        # Use regex union for efficiency: key~"^(val1|val2|...)$"
        value_regex = "^(" + "|".join(re.escape(v) for v in values) + ")$"
        union_parts.append(f'  nwr["{key}"~"{value_regex}"](area.searcharea);')

    union_block = "\n".join(union_parts)

    query = f"""[out:json][timeout:{timeout}];
area["name"="{area_name}"]->.searcharea;
(
{union_block}
);
out body center qt;
"""
    return query


# ─────────────────────────────────────────────
# OVERPASS FETCHER
# ─────────────────────────────────────────────

def fetch_overpass(query: str, retries: int = 3) -> list[dict]:
    """Execute an Overpass query and return the list of OSM elements."""
    for attempt in range(1, retries + 1):
        try:
            resp = requests.post(
                OVERPASS_ENDPOINT,
                data={"data": query},
                timeout=300,
                headers={"User-Agent": "meridian-directory-scraper/1.0"},
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("elements", [])
        except requests.exceptions.Timeout:
            log.warning(f"Overpass timeout on attempt {attempt}/{retries}")
        except requests.exceptions.HTTPError as e:
            if resp.status_code == 429:
                wait = 60 * attempt
                log.warning(f"Rate limited by Overpass. Waiting {wait}s...")
                time.sleep(wait)
            else:
                log.error(f"HTTP error: {e}")
                break
        except Exception as e:
            log.error(f"Overpass request failed: {e}")
            break
        if attempt < retries:
            time.sleep(5 * attempt)
    return []


# ─────────────────────────────────────────────
# RECORD NORMALISER
# ─────────────────────────────────────────────

def normalise(element: dict, category_key: str, scrape_date: str) -> dict | None:
    """Convert a raw OSM element into a Meridian-schema record dict.

    Returns None if the element lacks a name (unpublishable as a listing).
    """
    tags = element.get("tags", {})
    name = tags.get("name", "").strip()
    if not name:
        return None

    lat, lon = get_lat_lon(element)
    if lat is None or lon is None:
        lat = tags.get("lat")
        lon = tags.get("lon")

    cat = MERIDIAN_CATEGORIES[category_key]
    city_slug, area_slug = extract_city_area_from_tags(tags)
    address = build_address(tags)

    osm_type = element.get("type", "node")  # node / way / relation
    osm_id   = f"{osm_type}/{element.get('id', '')}"

    phone   = tags.get("phone") or tags.get("contact:phone") or tags.get("telephone") or ""
    website = tags.get("website") or tags.get("contact:website") or tags.get("url") or ""
    email   = tags.get("contact:email") or tags.get("email") or ""

    social_facebook  = tags.get("contact:facebook") or tags.get("facebook") or ""
    social_instagram = tags.get("contact:instagram") or tags.get("instagram") or ""
    social_twitter   = tags.get("contact:twitter") or tags.get("twitter") or ""
    social_tiktok    = tags.get("contact:tiktok") or tags.get("tiktok") or ""
    social_linkedin  = tags.get("contact:linkedin") or tags.get("linkedin") or ""
    social_youtube   = tags.get("contact:youtube") or tags.get("youtube") or ""

    wikidata_id = tags.get("wikidata", "")

    opening_hours = tags.get("opening_hours", "")

    chain_flag    = "chain" if is_chain(name) else "independent"
    ranking_tier  = "low" if chain_flag == "chain" else "standard"

    return {
        "osm_id":              osm_id,
        "name":                name,
        "category":            cat["label"],
        "category_key":        category_key,
        "category_slug":       cat["slug"],
        "address":             address,
        "city_slug":           city_slug,
        "area_slug":           area_slug,
        "business_slug":       slugify(name),
        "latitude":            lat,
        "longitude":           lon,
        "phone":               phone,
        "website":             website,
        "email":               email,
        "opening_hours":       opening_hours,
        "tags":                aggregate_tags(tags),
        "chain_flag":          chain_flag,
        "ranking_tier":        ranking_tier,
        "social_facebook":     social_facebook,
        "social_instagram":    social_instagram,
        "social_twitter":      social_twitter,
        "social_tiktok":       social_tiktok,
        "social_linkedin":     social_linkedin,
        "social_youtube":      social_youtube,
        "wikidata_id":         wikidata_id,
        # Google enrichment fields — left blank, populated by enrich_google.py
        "google_place_id":     "",
        "google_maps_url":     "",
        "photo_url":           "",
        "image_url":           "",
        "google_summary":      "",
        "google_rating":       "",
        "google_review_count": "",
        # FSA fields — left blank, populated by enrich_fsa.py
        "fsa_rating":              "",
        "fsa_hygiene_score":       "",
        "fsa_establishment_id":    "",
        # Metadata
        "status":              "pending",
        "source":              "OpenStreetMap",
        "scrape_date":         scrape_date,
        "last_synced_at":      datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }


# ─────────────────────────────────────────────
# CSV WRITER
# ─────────────────────────────────────────────

# Canonical CSV column order — must match Supabase schema
CSV_COLUMNS = [
    "osm_id", "name", "category", "category_key", "category_slug",
    "address", "city_slug", "area_slug", "business_slug",
    "latitude", "longitude",
    "phone", "website", "email", "opening_hours",
    "google_maps_url", "photo_url", "image_url",
    "google_summary", "google_rating", "google_review_count", "google_place_id",
    "tags", "chain_flag",
    "social_facebook", "social_instagram", "social_twitter",
    "social_tiktok", "social_linkedin", "social_youtube",
    "wikidata_id",
    "fsa_rating", "fsa_hygiene_score", "fsa_establishment_id",
    "status", "ranking_tier", "source", "scrape_date", "last_synced_at",
]


def save_csv(records: list[dict], output_path: str) -> None:
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for rec in records:
            row = {col: rec.get(col, "") for col in CSV_COLUMNS}
            writer.writerow(row)
    log.info(f"Saved {len(records)} records → {output_path}")


# ─────────────────────────────────────────────
# MAIN SCRAPE ORCHESTRATION
# ─────────────────────────────────────────────

def run_scrape(
    area_name: str,
    categories: list[str],
    timeout: int,
    dry_run: bool,
) -> list[dict]:
    """Fetch all businesses for the given area and categories from Overpass."""
    scrape_date = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    all_records: list[dict] = []
    seen_osm_ids: set[str] = set()

    for cat_key in categories:
        log.info(f"Querying OSM: area='{area_name}' category='{cat_key}'")
        query = build_overpass_query(area_name, cat_key, timeout=timeout)

        if dry_run:
            log.info(f"[DRY RUN] Would execute query:\n{query[:300]}...")
            continue

        elements = fetch_overpass(query)
        log.info(f"  Received {len(elements)} elements from Overpass")

        for el in elements:
            rec = normalise(el, cat_key, scrape_date)
            if rec is None:
                continue
            if rec["osm_id"] in seen_osm_ids:
                continue
            seen_osm_ids.add(rec["osm_id"])
            all_records.append(rec)

        # Brief pause between category queries to be a good Overpass citizen
        if len(categories) > 1:
            time.sleep(2)

    return all_records


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape business data from OpenStreetMap via Overpass API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--area", "-a",
        required=True,
        help='OSM admin area name, e.g. "City of Bristol" or "Greater Manchester"',
    )
    parser.add_argument(
        "--categories", "-c",
        default=",".join(MERIDIAN_CATEGORIES.keys()),
        help="Comma-separated category keys (default: all). "
             "Options: " + ", ".join(MERIDIAN_CATEGORIES.keys()),
    )
    parser.add_argument(
        "--output", "-o",
        default=None,
        help="Output CSV filename (default: auto-generated with timestamp)",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="Overpass query timeout in seconds (default: 180; use 900 for UK-wide)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print query and estimated counts; do not write any files",
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="List available category keys and exit",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list_categories:
        print("Available categories:")
        for k, v in MERIDIAN_CATEGORIES.items():
            print(f"  {k:<20} {v['label']}")
        return

    categories = [c.strip() for c in args.categories.split(",") if c.strip()]
    invalid = [c for c in categories if c not in MERIDIAN_CATEGORIES]
    if invalid:
        sys.exit(f"ERROR: Unknown categories: {invalid}. Use --list-categories to see options.")

    log.info(f"Area: {args.area}")
    log.info(f"Categories: {categories}")
    log.info(f"Timeout: {args.timeout}s")
    if args.dry_run:
        log.info("DRY RUN — no files will be written")

    records = run_scrape(
        area_name=args.area,
        categories=categories,
        timeout=args.timeout,
        dry_run=args.dry_run,
    )

    if args.dry_run:
        log.info(f"[DRY RUN] Would have produced {len(records)} records across {len(categories)} categories")
        return

    if not records:
        log.warning("No records found. Check the area name matches an OSM admin boundary.")
        return

    # Chains summary
    chains = sum(1 for r in records if r["chain_flag"] == "chain")
    log.info(f"Results: {len(records)} total ({len(records) - chains} independent, {chains} chain)")

    # Output filename
    if args.output:
        output_path = args.output
    else:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        area_slug = slugify(args.area)
        output_path = f"meridian_osm_{area_slug}_{ts}.csv"

    save_csv(records, output_path)

    # Sample preview
    if records:
        log.info("Sample records (first 3):")
        for rec in records[:3]:
            log.info(f"  {rec['name']} | {rec['category']} | {rec['address'][:50]}")


if __name__ == "__main__":
    main()
