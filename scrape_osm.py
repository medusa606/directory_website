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

    # Discover all tags in an area and suggest new categories
    python scrape_osm.py --area "City of Bristol" --discover-tags

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
    # Convenience & Supermarkets
    "Londis", "Spar", "Kwik Save", "Budgens",
    "Tesco", "Tesco Express", "Tesco Metro",
    "Sainsbury's", "Sainsbury's Local",
    "Asda", "Morrisons", "Morrisons Daily", "Waitrose", "Iceland", "Co-op",
    "Aldi", "Lidl", "Marks & Spencer", "M&S Food Hall", "M&S Simply Food", "Costco",
    "Ocado", "Poundland", "Home Bargains", "B&M", "The Range",
    # Coffee & Casual
    "Starbucks", "Costa Coffee", "Caffè Nero", "Caffe Nero",
    # Fast Food
    "McDonald's", "McDonalds", "Burger King", "KFC",
    "Subway", "Greggs", "Pret a Manger",
    # Casual Dining
    "Nando's", "Nandos", "Pizza Hut", "Domino's", "Dominos",
    "Pizza Express", "Wagamama", "Five Guys",
    "Wetherspoon", "Harvester", "Toby Carvery", "Zizzi", "Prezzo",
    # Banks
    "Barclays", "Lloyds Bank", "NatWest", "HSBC", "Santander", "Halifax",
    # Pharmacy & Health
    "Boots", "Boots Pharmacy", "Superdrug", "Lloyds Pharmacy", "Holland & Barrett",
    # DIY & Home
    "B&Q", "Homebase", "Wickes", "Screwfix", "Toolstation",
    # Mobile Carriers
    "Vodafone", "EE", "EE Store", "O2", "O2 Store", "Three", "Three Store",
    # Hotels
    "Premier Inn", "Travelodge", "Holiday Inn",
    # Fashion & Retail
    "Primark", "Next", "H&M", "Zara", "Sports Direct", "Wilko",
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
                                          "convenience", "farm", "organic", "spices", "seafood",
                                          "cafe", "kitchen", "takeaway"]},
            {"key": "amenity", "values": ["marketplace", "food_court", "restaurant"]},
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
            {"key": "amenity",     "values": ["spa", "massage", "sauna", "dentist", "doctor", "clinic", "pharmacy", "optician"]},
            {"key": "leisure",     "values": ["fitness_centre", "sports_centre", "yoga", "dance"]},
            {"key": "healthcare",  "values": ["alternative", "therapist", "herbalist",
                                               "acupuncture", "naturopath", "osteopath",
                                               "physiotherapist", "audiologist"]},
            {"key": "shop",        "values": ["nutrition_supplements", "herbalist", "massage",
                                               "wellness", "beauty", "hairdresser", "cosmetics", "hairdresser_supply"]},
        ],
    },
    "entertainment": {
        "label": "Entertainment",
        "slug": "entertainment",
        "osm_filters": [
            {"key": "amenity", "values": ["cinema", "theatre", "theater", "museum", "nightclub", "arcade"]},
            {"key": "leisure", "values": ["cinema", "museum", "theatre", "nightclub"]},
        ],
    },
    "fitness_sports": {
        "label": "Fitness & Sports",
        "slug": "fitness-and-sports",
        "osm_filters": [
            {"key": "leisure", "values": ["fitness_centre", "swimming_pool", "sports_centre", "bowling_alley", "climbing_wall", "golf_course", "track", "horse_riding", "ice_rink", "sports_hall"]},
            {"key": "amenity", "values": ["gym", "yoga"]},
        ],
    },
    "services": {
        "label": "Services",
        "slug": "services",
        "osm_filters": [
            {"key": "shop", "values": ["laundry", "dry_cleaning", "tailor", "repair", "shoemaker", "shoes", "key_maker", "locksmith", "watchmaker"]},
            {"key": "amenity", "values": ["laundry", "dry_cleaning"]},
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

def fetch_overpass(query: str, retries: int = 5) -> list[dict]:
    """Execute an Overpass query and return the list of OSM elements.
    
    Retries on transient errors (429 rate limit, 504 gateway timeout, timeouts).
    Uses exponential backoff to avoid overwhelming the server.
    """
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
            log.warning(f"Overpass timeout on attempt {attempt}/{retries}, retrying...")
            if attempt < retries:
                wait = 10 * (2 ** (attempt - 1))  # 10s, 20s, 40s, 80s, 160s
                log.info(f"  Waiting {wait}s before retry...")
                time.sleep(wait)
        except requests.exceptions.HTTPError as e:
            if resp.status_code in (429, 504):
                # 429: rate limited | 504: gateway timeout (server overloaded)
                # Both are transient — retry with exponential backoff
                wait = 10 * (2 ** (attempt - 1))
                log.warning(
                    f"Overpass {resp.status_code} on attempt {attempt}/{retries}, "
                    f"waiting {wait}s before retry..."
                )
                time.sleep(wait)
            else:
                # Other HTTP errors are not recoverable
                log.error(f"HTTP error {resp.status_code}: {e}")
                break
        except Exception as e:
            log.error(f"Overpass request failed: {e}")
            break
    
    log.error(f"Overpass query failed after {retries} retries")
    return []


# ─────────────────────────────────────────────
# TAG DISCOVERY
# ─────────────────────────────────────────────

def discover_tags(area_name: str) -> dict:
    """Query Overpass to find all business-related tags in the area.
    
    Returns a dict with tag keys and their value counts:
    {
        "amenity": {"restaurant": 150, "cafe": 80, ...},
        "shop": {"bakery": 45, "butcher": 20, ...},
        ...
    }
    """
    # Query for all business-related tag keys
    query = f"""
[out:json][timeout:300];
area["name"="{area_name}"]->.searcharea;
(
  node[amenity](area.searcharea);
  node[shop](area.searcharea);
  node[craft](area.searcharea);
  node[leisure](area.searcharea);
  node[healthcare](area.searcharea);
  node[tourism](area.searcharea);
  way[amenity](area.searcharea);
  way[shop](area.searcharea);
  way[craft](area.searcharea);
  way[leisure](area.searcharea);
  way[healthcare](area.searcharea);
  way[tourism](area.searcharea);
);
out tags;
"""
    log.info("Discovering tags in area (this may take a minute)...")
    elements = fetch_overpass(query, retries=3)
    log.info(f"  Retrieved {len(elements)} elements")

    # Aggregate by key → value → count
    tag_counts = {}
    for el in elements:
        tags = el.get("tags", {})
        for key in ("amenity", "shop", "craft", "leisure", "healthcare", "tourism"):
            value = tags.get(key)
            if value:
                if key not in tag_counts:
                    tag_counts[key] = {}
                # Handle multiple values separated by semicolon
                for v in value.split(";"):
                    v = v.strip()
                    if v:
                        tag_counts[key][v] = tag_counts[key].get(v, 0) + 1

    return tag_counts


def get_currently_captured_tags() -> dict:
    """Return set of all tag values currently captured by our categories.
    
    Returns dict: {"amenity": {set of values}, "shop": {set}, ...}
    """
    captured = {}
    for cat_key, cat in MERIDIAN_CATEGORIES.items():
        for f in cat.get("osm_filters", []):
            key = f["key"]
            values = set(f["values"])
            if key not in captured:
                captured[key] = set()
            captured[key].update(values)
    return captured


def analyze_tag_gaps(tag_counts: dict, captured: dict) -> dict:
    """Find tags not in our current categories and group by semantic meaning.
    
    Returns dict: {"new_category_suggestion": {"values": [...], "count": N}, ...}
    """
    uncaptured = {}
    
    for key, value_counts in tag_counts.items():
        captured_values = captured.get(key, set())
        for value, count in value_counts.items():
            if value not in captured_values:
                if value not in uncaptured:
                    uncaptured[value] = {"key": key, "count": count, "category": None}

    # Semantic grouping of uncaptured tags
    semantic_groups = {
        "Beauty & Personal Care": {
            "patterns": [
                "hair", "beauty", "cosmetics", "salon", "barber", "nail",
                "esthetic", "beautician", "makeup", "grooming"
            ],
        },
        "Health & Medical": {
            "patterns": [
                "dentist", "doctor", "clinic", "hospital", "pharmacy",
                "optician", "physiotherapy", "veterinary", "medical"
            ],
        },
        "Fitness & Sports": {
            "patterns": [
                "gym", "fitness", "swimming", "pool", "track", "court",
                "climbing", "bowling", "skateboard", "golf"
            ],
        },
        "Entertainment": {
            "patterns": [
                "cinema", "theater", "theatre", "museum", "exhibition",
                "nightclub", "karaoke", "arcade"
            ],
        },
        "Services": {
            "patterns": [
                "laundry", "dry_cleaning", "repair", "tailor", "shoemaker",
                "key_maker", "locksmith", "watchmaker"
            ],
        },
        "Food & Hospitality": {
            "patterns": [
                "bakery", "butcher", "cafe", "restaurant", "food", "kitchen",
                "takeaway", "food_court"
            ],
        },
    }

    # Assign uncaptured tags to semantic groups
    assigned = {}
    for value, info in uncaptured.items():
        for group_name, group_data in semantic_groups.items():
            if any(pattern in value.lower() for pattern in group_data["patterns"]):
                if group_name not in assigned:
                    assigned[group_name] = []
                assigned[group_name].append((value, info["count"], info["key"]))
                break

    return assigned


def print_discovery_report(tag_counts: dict, captured: dict, assigned: dict):
    """Print a formatted report of tag discovery."""
    print("\n" + "=" * 80)
    print("OSM TAG DISCOVERY REPORT".center(80))
    print("=" * 80)

    # Part 1: Current coverage
    print("\n[CURRENT COVERAGE BY KEY]")
    for key in ["amenity", "shop", "craft", "leisure", "healthcare", "tourism"]:
        captured_count = len(captured.get(key, set()))
        total_count = len(tag_counts.get(key, {}))
        coverage_pct = (captured_count / total_count * 100) if total_count > 0 else 0
        print(f"  {key:<15} {captured_count:>3} / {total_count:>3} tags captured ({coverage_pct:>5.1f}%)")

    # Part 2: Current categories
    print("\n[CURRENT MERIDIAN CATEGORIES ({} total)]".format(len(MERIDIAN_CATEGORIES)))
    for cat_key, cat in MERIDIAN_CATEGORIES.items():
        values_count = sum(len(f["values"]) for f in cat.get("osm_filters", []))
        print(f"  {cat_key:<20} {values_count:>3} tag values  →  {cat['label']}")

    # Part 3: Suggested new categories
    print("\n[SUGGESTED NEW CATEGORIES FROM UNCAPTURED TAGS]")
    total_uncaptured = 0
    for group_name in sorted(assigned.keys()):
        values = assigned[group_name]
        total_uncaptured += len(values)
        count_sum = sum(v[1] for v in values)  # Sum of occurrences
        print(f"\n  📌 {group_name} ({len(values)} new tags, {count_sum} total occurrences)")
        # Show top 5 most common uncaptured tags in this group
        sorted_values = sorted(values, key=lambda x: x[1], reverse=True)
        for value, count, key in sorted_values[:5]:
            print(f"      • {value:<25} (key={key}, count={count})")
        if len(sorted_values) > 5:
            print(f"      ... and {len(sorted_values) - 5} more")

    print("\n" + "=" * 80)
    print(f"SUMMARY: {total_uncaptured} uncaptured tags found across {len(assigned)} semantic groups")
    print("=" * 80 + "\n")


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

        # Pause between category queries to be a good Overpass citizen
        # Overpass appreciates spacing; queries are already slow (5-30s each)
        if len(categories) > 1:
            time.sleep(5)

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
        default=None,
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
    parser.add_argument(
        "--discover-tags",
        action="store_true",
        help="Discover all business-related tags in the area and suggest new categories",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.list_categories:
        print("Available categories:")
        for k, v in MERIDIAN_CATEGORIES.items():
            print(f"  {k:<20} {v['label']}")
        return

    if args.discover_tags:
        if not args.area:
            sys.exit("ERROR: --discover-tags requires --area")
        tag_counts = discover_tags(args.area)
        if not tag_counts:
            log.error("No tags found. Check that the area name is correct.")
            return
        captured = get_currently_captured_tags()
        assigned = analyze_tag_gaps(tag_counts, captured)
        print_discovery_report(tag_counts, captured, assigned)
        return

    if not args.area:
        sys.exit("ERROR: --area is required for scraping")

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
