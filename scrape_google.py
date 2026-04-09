"""
scrape_google.py — Meridian Directory
======================================
Scrapes local business data from the Google Places API and writes
candidate records to Airtable (or a local CSV for review).

USAGE EXAMPLES
--------------
# By place name, 1km radius:
  python scrape_google.py --location "Hebden Bridge, West Yorkshire" --radius 1000

# By postcode, 2km radius, specific categories only:
  python scrape_google.py --postcode "HX7 8AB" --radius 2000 --categories "food_produce,craft_makers"

# By lat/lng (useful when running from another script):
  python scrape_google.py --latlng "53.7440,-2.0110" --radius 1500

# Dry run — print results to terminal, don't push to Airtable:
  python scrape_google.py --location "Todmorden" --radius 2000 --dry-run

# Save to CSV only (no Airtable):
  python scrape_google.py --location "Sowerby Bridge" --radius 1500 --output csv

# Scrape with a 50-result cutoff
python scrape_google.py --location "Hebden Bridge" --radius 2000 --max-results 50

# Scrape to CSV only, review it, then push later
python scrape_google.py --location "Todmorden" --radius 1500 --output csv --max-results 100

# ... review and edit the CSV ...
python scrape_google.py --push-csv meridian_candidates_20260406_1711.csv

# Combine cutoff with specific categories
python scrape_google.py --postcode "HX7 8AB" --radius 1000 --categories "food_produce,craft_makers" --max-results 30


SETUP
-----
  pip install requests python-dotenv pyairtable geopy

  Create a .env file in the same directory:
    GOOGLE_PLACES_API_KEY=your_key_here
    AIRTABLE_API_KEY=your_key_here
    AIRTABLE_BASE_ID=your_base_id_here
    AIRTABLE_TABLE_NAME=Candidates
"""

import os
import sys
import csv
import time
import json
import argparse
import logging
from pathlib import Path

import requests
from dotenv import load_dotenv
from geopy.geocoders import Nominatim
from datetime import datetime, timezone


import math

def haversine_metres(lat1, lng1, lat2, lng2):
    """Calculate distance in metres between two lat/lng points."""
    R = 6371000  # Earth's radius in metres
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lng2 - lng1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) *
         math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

# ── Try importing Airtable; gracefully degrade to CSV if not installed ──
try:
    from pyairtable import Api as AirtableApi
    AIRTABLE_AVAILABLE = True
except ImportError:
    AIRTABLE_AVAILABLE = False

# ─────────────────────────────────────────────
# MERIDIAN BUSINESS CATEGORIES
# Each entry maps a Meridian display name to the
# Google Places types used to find those businesses.
# ─────────────────────────────────────────────
MERIDIAN_CATEGORIES = {

    # ── Food & Drink ──────────────────────────
    "food_produce": {
        "label": "Food & Produce",
        "google_types": [
            "bakery", "butcher", "grocery_or_supermarket",
            "food", "meal_takeaway", "cafe",
        ],
        "keywords": ["farm shop", "deli", "delicatessen", "fishmonger",
                     "greengrocer", "cheese", "charcuterie", "market stall"],
    },
    "restaurants_cafes": {
        "label": "Restaurants & Cafés",
        "google_types": ["restaurant", "cafe", "bar", "meal_delivery"],
        "keywords": ["supper club", "pop-up restaurant", "street food"],
    },
    "drinks_brewing": {
        "label": "Drinks & Brewing",
        "google_types": ["bar", "liquor_store"],
        "keywords": ["brewery", "microbrewery", "distillery", "gin", "cider",
                     "winery", "wine merchant", "craft beer", "kombucha"],
    },

    # ── Craft & Making ────────────────────────
    "craft_makers": {
        "label": "Craft & Makers",
        "google_types": ["art_gallery", "store"],
        "keywords": ["ceramics", "pottery", "woodworker", "blacksmith",
                     "jeweller", "jewellery", "silversmith", "weaver",
                     "glassblower", "printmaker", "leather", "bookbinder",
                     "candle", "soap maker", "textile"],
    },
    "art_design": {
        "label": "Art & Design",
        "google_types": ["art_gallery", "painter"],
        "keywords": ["artist", "illustrator", "graphic designer", "sculptor",
                     "photographer", "printmaker", "muralist", "studio"],
    },
    "fashion_clothing": {
        "label": "Fashion & Clothing",
        "google_types": ["clothing_store", "shoe_store"],
        "keywords": ["dressmaker", "tailor", "seamstress", "milliner",
                     "sustainable fashion", "vintage clothing", "alteration"],
    },

    # ── Home & Garden ─────────────────────────
    "home_interiors": {
        "label": "Home & Interiors",
        "google_types": ["furniture_store", "home_goods_store", "interior_designer"],
        "keywords": ["interior design", "upholstery", "antiques",
                     "vintage furniture", "restoration", "cabinet maker"],
    },
    "plants_garden": {
        "label": "Plants & Garden",
        "google_types": ["florist", "garden_center", "landscaping"],
        "keywords": ["nursery", "horticulture", "landscape gardener",
                     "garden design", "wildflower", "allotment"],
    },
    "building_trades": {
        "label": "Building & Trades",
        "google_types": ["electrician", "plumber", "roofing_contractor",
                         "general_contractor", "painter"],
        "keywords": ["builder", "carpenter", "joiner", "stonemason",
                     "plasterer", "tiler", "roofer", "glazier",
                     "heating engineer", "solar installer"],
    },

    # ── Wellbeing & Care ──────────────────────
    "health_wellbeing": {
        "label": "Health & Wellbeing",
        "google_types": ["physiotherapist", "gym", "spa", "beauty_salon"],
        "keywords": ["osteopath", "acupuncture", "massage therapist",
                     "yoga teacher", "pilates", "nutritionist",
                     "herbalist", "naturopath", "counsellor", "therapist"],
    },
    "hair_beauty": {
        "label": "Hair & Beauty",
        "google_types": ["hair_care", "beauty_salon", "spa"],
        "keywords": ["barber", "hairdresser", "nail technician",
                     "mobile beautician", "makeup artist"],
    },
    "childcare_education": {
        "label": "Childcare & Education",
        "google_types": ["school", "secondary_school", "tutoring"],
        "keywords": ["childminder", "nursery", "tutor", "music teacher",
                     "art classes", "drama school", "language tutor"],
    },

    # ── Services ──────────────────────────────
    "professional_services": {
        "label": "Professional Services",
        "google_types": ["lawyer", "accountant", "insurance_agency",
                         "finance", "real_estate_agency"],
        "keywords": ["solicitor", "bookkeeper", "financial advisor",
                     "architect", "surveyor", "planning consultant"],
    },
    "tech_digital": {
        "label": "Tech & Digital",
        "google_types": ["electronics_store"],
        "keywords": ["web designer", "developer", "IT support",
                     "app developer", "digital marketing", "SEO",
                     "videographer", "podcast studio"],
    },
    "repair_restoration": {
        "label": "Repair & Restoration",
        "google_types": ["bicycle_store", "car_repair"],
        "keywords": ["cobbler", "shoe repair", "watch repair", "clockmaker",
                     "bicycle repair", "appliance repair", "phone repair",
                     "furniture restoration", "clothing repair"],
    },

    # ── Community & Culture ───────────────────
    "music_performance": {
        "label": "Music & Performance",
        "google_types": ["night_club", "movie_theater"],
        "keywords": ["music teacher", "recording studio", "sound engineer",
                     "venue", "theatre company", "dance teacher",
                     "choir", "band", "DJ"],
    },
    "books_publishing": {
        "label": "Books & Publishing",
        "google_types": ["book_store", "library"],
        "keywords": ["bookshop", "publisher", "writer", "editor",
                     "zine", "independent press", "illustrator"],
    },
    "community_social": {
        "label": "Community & Social Enterprise",
        "google_types": ["local_government_office", "church"],
        "keywords": ["community group", "social enterprise", "cooperative",
                     "charity", "food bank", "repair café", "community garden",
                     "mutual aid", "community hub"],
    },

    # ── Animals & Nature ──────────────────────
    "animals_pets": {
        "label": "Animals & Pets",
        "google_types": ["veterinary_care", "pet_store"],
        "keywords": ["dog trainer", "dog groomer", "pet sitter",
                     "farrier", "horse riding", "animal sanctuary"],
    },

    # ── Accommodation & Experience ────────────
    "accommodation": {
        "label": "Accommodation",
        "google_types": ["lodging", "bed_and_breakfast"],
        "keywords": ["B&B", "guesthouse", "holiday cottage", "glamping",
                     "shepherd's hut", "airbnb host", "self-catering"],
    },
    "experiences_tours": {
        "label": "Experiences & Tours",
        "google_types": ["tourist_attraction", "travel_agency"],
        "keywords": ["walking guide", "foraging", "cookery class",
                     "craft workshop", "art class", "tour guide",
                     "outdoor education", "bushcraft"],
    },
}

# ─────────────────────────────────────────────
# GOOGLE PLACES API HELPERS
# ─────────────────────────────────────────────

PLACES_NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
PLACES_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
PLACES_TEXT_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

# Fields to fetch in Place Details (minimise billable fields)
DETAIL_FIELDS = ",".join([
    "place_id", "name", "formatted_address", "formatted_phone_number",
    "international_phone_number", "website", "url",
    "opening_hours", "photos", "geometry",
    "rating", "user_ratings_total",
    "business_status", "types",
    "editorial_summary",
])


def geocode_location(query: str, api_key: str) -> tuple[float, float] | None:
    """Convert a place name or postcode to lat/lng using Google Geocoding."""
    resp = requests.get(GEOCODE_URL, params={"address": query, "key": api_key}, timeout=10)
    data = resp.json()
    if data.get("status") == "OK":
        loc = data["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    logging.warning(f"Geocoding failed for '{query}': {data.get('status')}")
    return None


def geocode_postcode_nominatim(postcode: str) -> tuple[float, float] | None:
    """Fallback: geocode a UK postcode via Nominatim (free, no key)."""
    geolocator = Nominatim(user_agent="meridian-scraper")
    try:
        location = geolocator.geocode(postcode, country_codes="GB", timeout=10)
        if location:
            return location.latitude, location.longitude
    except Exception as e:
        logging.warning(f"Nominatim geocoding failed: {e}")
    return None


def nearby_search(lat: float, lng: float, radius: int,
                  place_type: str, api_key: str) -> list[dict]:
    """
    Run a Nearby Search for a single Google place type.
    Handles pagination automatically (up to 3 pages = ~60 results).
    """
    results = []
    params = {
        "location": f"{lat},{lng}",
        "radius": radius,
        "type": place_type,
        "key": api_key,
    }
    page = 0
    while page < 3:
        resp = requests.get(PLACES_NEARBY_URL, params=params, timeout=10)
        data = resp.json()
        status = data.get("status")
        if status not in ("OK", "ZERO_RESULTS"):
            logging.warning(f"Places API error ({place_type}): {status}")
            break
        results.extend(data.get("results", []))
        next_token = data.get("next_page_token")
        if not next_token:
            break
        # Google requires a short delay before using the next_page_token
        time.sleep(2)
        params = {"pagetoken": next_token, "key": api_key}
        page += 1

    return results


def text_search(lat: float, lng: float, radius: int,
                keyword: str, api_key: str) -> list[dict]:
    """
    Text Search for a keyword (e.g. 'artisan baker', 'ceramics studio').
    Useful for categories not well-covered by Google's type taxonomy.
    """
    results = []
    params = {
        "query": keyword,
        "location": f"{lat},{lng}",
        "radius": radius,
        "key": api_key,
    }
    resp = requests.get(PLACES_TEXT_URL, params=params, timeout=10)
    data = resp.json()
    if data.get("status") == "OK":
        results.extend(data.get("results", []))
    return results


def get_place_details(place_id: str, api_key: str) -> dict:
    """Fetch full details for a place by its place_id."""
    params = {
        "place_id": place_id,
        "fields": DETAIL_FIELDS,
        "key": api_key,
    }
    resp = requests.get(PLACES_DETAILS_URL, params=params, timeout=10)
    data = resp.json()
    if data.get("status") == "OK":
        return data.get("result", {})
    return {}


def build_photo_url(photo_reference: str, api_key: str, max_width: int = 800) -> str:
    """Build a URL to fetch a Place photo."""
    return (
        f"https://maps.googleapis.com/maps/api/place/photo"
        f"?maxwidth={max_width}&photo_reference={photo_reference}&key={api_key}"
    )


# ─────────────────────────────────────────────
# CHAIN / CORPORATE DETECTION
# Meridian only lists independent, local businesses.
# Rather than auto-skipping (which risks false positives),
# we flag suspected chains for human review.
# ─────────────────────────────────────────────

KNOWN_CHAINS = {
    # Supermarkets
    "tesco", "tesco express", "tesco metro",
    "sainsbury's", "sainsbury's local",
    "asda", "morrisons", "waitrose",
    "lidl", "aldi", "marks & spencer", "m&s simply food",
    "co-op", "costco", "iceland",
    # Coffee / fast food
    "starbucks", "costa coffee", "caffe nero",
    "mcdonald's", "mcdonalds", "burger king", "kfc",
    "subway", "greggs", "pret a manger",
    "nando's", "nandos", "pizza hut",
    "domino's", "dominos", "pizza express",
    "wagamama", "five guys", "leon",
    # Banks / finance
    "barclays", "lloyds bank", "natwest", "hsbc",
    "santander", "halifax", "nationwide",
    # Pharmacy / health
    "boots pharmacy", "boots opticians",
    "superdrug", "lloyds pharmacy",
    # DIY / home
    "b&q", "homebase", "wickes",
    "screwfix", "toolstation",
    # Telecoms
    "vodafone", "ee store", "o2 store",
    "three store", "bt shop",
    # Hotels
    "premier inn", "travelodge", "holiday inn",
    "ibis", "ibis budget",
    # Retail chains
    "primark", "next", "h&m", "zara",
    "sports direct", "wilko",
}


def detect_chain_flag(name: str) -> str:
    """
    Check if a business name looks like a known chain.
    Returns a flag string for the curator, or empty string if clean.

    Uses EXACT match on the full normalised name, plus a STARTS-WITH
    check for chains that have location suffixes
    (e.g. "Tesco Express - Hebden Bridge").
    """
    name_clean = name.lower().strip()

    # Remove common suffixes Google adds
    for suffix in [" - ", " – ", " (", " /"]:
        if suffix in name_clean:
            name_clean = name_clean[:name_clean.index(suffix)].strip()

    # Exact match
    if name_clean in KNOWN_CHAINS:
        return f"Exact match: '{name_clean}'"

    # Starts-with match (catches "Tesco Express - High Street" etc.)
    for chain in KNOWN_CHAINS:
        if name_clean.startswith(chain):
            return f"Starts with: '{chain}'"

    return ""

def is_chain(name: str) -> bool:
    """Return True if the business name matches a known chain."""
    name_lower = name.lower().strip()
    for chain in EXCLUDED_CHAINS:
        if chain in name_lower:
            return True
    return False


def is_permanently_closed(place: dict) -> bool:
    return place.get("business_status") == "CLOSED_PERMANENTLY"


# ─────────────────────────────────────────────
# NORMALISE TO MERIDIAN SCHEMA
# ─────────────────────────────────────────────

def normalise(place: dict, details: dict,
              meridian_category: str, api_key: str) -> dict:

    """
    Map Google Places data to the Meridian candidate schema.
    This matches the fields expected by airtable_push.py.
    """
    name = details.get("name") or place.get("name", "")
    address = details.get("formatted_address") or place.get("vicinity", "")
    phone = details.get("formatted_phone_number", "")
    website = details.get("website", "")
    maps_url = details.get("url", "")
    rating = details.get("rating", "")
    review_count = details.get("user_ratings_total", "")
    google_types = ", ".join(details.get("types") or place.get("types", []))
    editorial = details.get("editorial_summary", {}).get("overview", "")

    geo = (details.get("geometry") or place.get("geometry", {})).get("location", {})
    lat = geo.get("lat", "")
    lng = geo.get("lng", "")

    # Build photo URL from first available photo
    photos = details.get("photos") or place.get("photos", [])
    photo_url = ""
    if photos:
        ref = photos[0].get("photo_reference", "")
        if ref:
            photo_url = build_photo_url(ref, api_key)

    # Opening hours as a readable string
    hours_text = ""
    hours = details.get("opening_hours", {})
    if hours.get("weekday_text"):
        hours_text = " | ".join(hours["weekday_text"])

    category_label = MERIDIAN_CATEGORIES.get(meridian_category, {}).get("label", meridian_category)

    # Detect chain — flag for reviewer, don't auto-exclude
    chain_flag = detect_chain_flag(name)

    return {
        # Core identity
        "Name": name,
        "Category": category_label,
        "Category Key": meridian_category,
        "Address": address,
        "Latitude": lat,
        "Longitude": lng,
        # Contact
        "Phone": phone,
        "Website": website,
        "Google Maps URL": maps_url,
        # Media
        "Photo URL (raw)": photo_url,
        # Editorial
        "Google Summary": editorial,
        "Opening Hours": hours_text,
        # Metadata
        "Google Rating": rating,
        "Google Review Count": review_count,
        "Google Types (raw)": google_types,
        "Google Place ID": details.get("place_id") or place.get("place_id", ""),
        "Source": "Google Places",
        "Scrape Date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "last_synced_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        # Curation fields
        "Status": "Pending",
        "Chain Flag": chain_flag,  # ← new field
        "Editor Notes": "",
        "Story Draft": "",
    }


# ─────────────────────────────────────────────
# AIRTABLE PUSH
# ─────────────────────────────────────────────

def push_to_airtable(records: list[dict], api_key: str,
                     base_id: str, table_name: str) -> None:
    """
    Upsert records to Airtable, matching on 'Google Place ID' to
    avoid duplicating existing candidates.
    """
    if not AIRTABLE_AVAILABLE:
        logging.error("pyairtable not installed. Run: pip install pyairtable")
        return

    api = AirtableApi(api_key)
    table = api.table(base_id, table_name)

    # Fetch existing Place IDs to detect duplicates
    existing = table.all(fields=["Google Place ID"])
    existing_ids = {
        r["fields"].get("Google Place ID")
        for r in existing
        if r["fields"].get("Google Place ID")
    }

    new_records = [r for r in records if r.get("Google Place ID") not in existing_ids]
    skipped = len(records) - len(new_records)

    logging.info(f"  {len(new_records)} new records to push, {skipped} already exist — skipping.")

    if not new_records:
        return

    # ── Clean records for Airtable ──
    # Number fields reject empty strings — remove them entirely
    # so Airtable treats them as blank
    NUMERIC_FIELDS = {
        "Latitude", "Longitude", "Google Rating",
        "Google Review Count", "Distance (m)",
    }

    clean_records = []
    for record in new_records:
        clean = {}
        for key, value in record.items():
            # Skip empty values for numeric fields
            if key in NUMERIC_FIELDS:
                if value is None or value == "" or value == "None":
                    continue  # omit the field entirely
                try:
                    clean[key] = float(value)
                except (ValueError, TypeError):
                    continue  # can't parse — omit it
            else:
                if value is None:
                    clean[key] = ""
                else:
                    clean[key] = str(value)
        clean_records.append(clean)
    new_records = clean_records

    # Batch in groups of 10 (Airtable limit)
    for i in range(0, len(new_records), 10):
        batch = new_records[i:i + 10]
        table.batch_create(batch)
        time.sleep(0.25)  # stay within Airtable rate limits

    logging.info(f"  ✓ Pushed {len(new_records)} records to Airtable.")


# ─────────────────────────────────────────────
# CSV EXPORT
# ─────────────────────────────────────────────

def save_to_csv(records: list[dict], filepath: str) -> None:
    if not records:
        logging.info("No records to save.")
        return
    fieldnames = list(records[0].keys())
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    logging.info(f"  ✓ Saved {len(records)} records to {filepath}")


# ─────────────────────────────────────────────
# MAIN SCRAPE RUNNER
# ─────────────────────────────────────────────

# def run_scrape(lat: float, lng: float, radius: int,
#                category_keys: list[str], api_key: str,
#                max_details: int = 200) -> list[dict]:
#     """
#     Core scrape loop. For each requested category:
#       1. Run Nearby Search for each Google type
#       2. Run Text Search for each keyword
#       3. Deduplicate by place_id
#       4. Fetch full details for each unique place
#       5. Filter chains, closed businesses
#       6. Normalise to Meridian schema
#     """
#     all_places: dict[str, tuple[dict, str]] = {}  # place_id → (place, category_key)
#
#     for cat_key in category_keys:
#         cat = MERIDIAN_CATEGORIES.get(cat_key)
#         if not cat:
#             logging.warning(f"Unknown category key: {cat_key} — skipping.")
#             continue
#
#         logging.info(f"\n── Scraping category: {cat['label']} ──")
#
#         # Nearby search by type
#         for gtype in cat["google_types"]:
#             logging.info(f"  Nearby search: type={gtype}")
#             results = nearby_search(lat, lng, radius, gtype, api_key)
#             logging.info(f"    → {len(results)} raw results")
#             for p in results:
#                 pid = p.get("place_id")
#                 if pid and pid not in all_places:
#                     all_places[pid] = (p, cat_key)
#             time.sleep(0.5)
#
#         # Text search by keyword
#         for kw in cat["keywords"]:
#             logging.info(f"  Text search: '{kw}'")
#             results = text_search(lat, lng, radius, kw, api_key)
#             logging.info(f"    → {len(results)} raw results")
#             for p in results:
#                 pid = p.get("place_id")
#                 if pid and pid not in all_places:
#                     all_places[pid] = (p, cat_key)
#             time.sleep(0.5)
#
#     logging.info(f"\n── {len(all_places)} unique places found before filtering ──")
#
#     # Fetch details + filter + normalise
#     normalised = []
#     details_fetched = 0
#
#     for place_id, (place, cat_key) in all_places.items():
#         name = place.get("name", "")
#
#         # Pre-filter before spending a Details API call
#         if is_permanently_closed(place):
#             logging.debug(f"  SKIP (closed): {name}")
#             continue
#
#         if details_fetched >= max_details:
#             logging.warning(f"  Reached max_details limit ({max_details}). Stopping early.")
#             break
#
#         logging.info(f"  Fetching details: {name}")
#         details = get_place_details(place_id, api_key)
#         details_fetched += 1
#
#         record = normalise(place, details, cat_key, api_key)
#
#         # Enforce strict radius — Google treats radius as a bias, not a boundary
#         record_lat = record.get("Latitude")
#         record_lng = record.get("Longitude")
#         if record_lat and record_lng:
#             distance = haversine_metres(lat, lng, float(record_lat), float(record_lng))
#             record["Distance (m)"] = round(distance)
#             if distance > radius:
#                 logging.info(f"  SKIP (out of radius): {name} — {round(distance)}m away")
#                 continue
#         else:
#             record["Distance (m)"] = ""
#
#         normalised.append(record)
#         time.sleep(0.1)  # gentle rate limiting
#
#     logging.info(f"\n── {len(normalised)} candidate records after filtering ──")
#     return normalised

def run_scrape(lat: float, lng: float, radius: int,
               category_keys: list[str], api_key: str,
               max_details: int = 200,
               max_results: int = None,
               airtable_config: dict = None) -> list[dict]:

    all_places: dict[str, tuple[dict, str]] = {}
    normalised = []
    details_fetched = 0

    for cat_key in category_keys:
        cat = MERIDIAN_CATEGORIES.get(cat_key)
        if not cat:
            continue

        # ── Early exit if we already have enough ──
        if max_results and len(normalised) >= max_results:
            logging.info(f"  Reached {max_results} results — stopping early.")
            break

        logging.info(f"\n── Scraping category: {cat['label']} ──")
        category_places = {}

        # Nearby search by type
        for gtype in cat["google_types"]:
            if max_results and len(normalised) >= max_results:
                break
            logging.info(f"  Nearby search: type={gtype}")
            results = nearby_search(lat, lng, radius, gtype, api_key)
            logging.info(f"    → {len(results)} raw results")
            for p in results:
                pid = p.get("place_id")
                if pid and pid not in all_places:
                    all_places[pid] = (p, cat_key)
                    category_places[pid] = (p, cat_key)
            time.sleep(0.5)

        # Text search by keyword
        for kw in cat["keywords"]:
            if max_results and len(normalised) >= max_results:
                break
            logging.info(f"  Text search: '{kw}'")
            results = text_search(lat, lng, radius, kw, api_key)
            logging.info(f"    → {len(results)} raw results")
            for p in results:
                pid = p.get("place_id")
                if pid and pid not in all_places:
                    all_places[pid] = (p, cat_key)
                    category_places[pid] = (p, cat_key)
            time.sleep(0.5)

        # Fetch details + normalise for this category
        for place_id, (place, ckey) in category_places.items():
            if max_results and len(normalised) >= max_results:
                break
            if details_fetched >= max_details:
                logging.warning(f"  Reached max_details limit ({max_details}).")
                break

            name = place.get("name", "")
            if is_permanently_closed(place):
                logging.debug(f"  SKIP (closed): {name}")
                continue

            logging.info(f"  Fetching details: {name}")
            details = get_place_details(place_id, api_key)
            details_fetched += 1

            # Relevance check — is this actually the right kind of business?
            if not is_relevant(place, details, ckey):
                logging.info(f"  SKIP (not relevant to {ckey}): {name}")
                continue

            record = normalise(place, details, ckey, api_key)

            # Enforce strict radius
            record_lat = record.get("Latitude")
            record_lng = record.get("Longitude")
            if record_lat and record_lng:
                distance = haversine_metres(lat, lng, float(record_lat), float(record_lng))
                record["Distance (m)"] = round(distance)
                if distance > radius:
                    logging.info(f"  SKIP (out of radius): {name} — {round(distance)}m away")
                    continue
            else:
                record["Distance (m)"] = ""

            normalised.append(record)
            time.sleep(0.1)

        # Push per category if airtable config provided
        if airtable_config:
            cat_records = [r for r in normalised if r.get("Category Key") == cat_key]
            if cat_records:
                push_to_airtable(
                    cat_records,
                    airtable_config["key"],
                    airtable_config["base"],
                    airtable_config["table"],
                )

    logging.info(f"\n── {len(normalised)} candidate records after filtering ──")
    logging.info(f"── {details_fetched} Details API calls made ──")
    return normalised


# ─────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────

def parse_args():
    parser = argparse.ArgumentParser(
        description="Meridian — Google Places scraper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Location (mutually exclusive group — pick one)
    loc_group = parser.add_mutually_exclusive_group(required=False)
    loc_group.add_argument(
        "--location", "-l",
        help='Place name to geocode, e.g. "Hebden Bridge, West Yorkshire"',
    )
    loc_group.add_argument(
        "--postcode", "-p",
        help='UK postcode, e.g. "HX7 8AB"',
    )
    loc_group.add_argument(
        "--latlng",
        help='Lat/lng as "lat,lng", e.g. "53.744,-2.011"',
    )

    # Search radius
    parser.add_argument(
        "--radius", "-r",
        type=int,
        default=2000,
        help="Search radius in metres (default: 2000). Max: 50000.",
    )

    # Categories
    cat_keys = list(MERIDIAN_CATEGORIES.keys())
    parser.add_argument(
        "--categories", "-c",
        default="all",
        help=(
            'Comma-separated category keys to scrape, or "all". '
            f'Available: {", ".join(cat_keys)}'
        ),
    )

    # Output
    parser.add_argument(
        "--output", "-o",
        choices=["airtable", "csv", "both"],
        default="both",
        help="Where to send results (default: both)",
    )
    parser.add_argument(
        "--csv-path",
        default=None,
        help="Custom CSV output path (default: meridian_candidates_YYYYMMDD.csv)",
    )

    # Limits
    parser.add_argument(
        "--max-details",
        type=int,
        default=200,
        help="Max number of Places Detail API calls per run (default: 200)",
    )

    # Flags
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print results to terminal only; do not write to Airtable or CSV",
    )
    parser.add_argument(
        "--list-categories",
        action="store_true",
        help="Print all available category keys and exit",
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable debug-level logging",
    )
    # Results cutoff
    parser.add_argument(
        "--max-results",
        type=int,
        default=None,
        help=(
            "Maximum number of final results to keep. "
            "Prioritises closest to search centre, then highest rated. "
            "Applied after all filtering."
        ),
    )

    # Push existing CSV to Airtable
    parser.add_argument(
        "--push-csv",
        type=str,
        default=None,
        help=(
            "Path to an existing Meridian CSV file to push to Airtable. "
            "Skips scraping entirely. "
            "Example: --push-csv meridian_candidates_20260406.csv"
        ),
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Logging setup
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )

    if args.list_categories:
        print("\nMeridian Business Categories\n" + "─" * 40)
        for key, cat in MERIDIAN_CATEGORIES.items():
            print(f"  {key:<28} {cat['label']}")
        print()
        sys.exit(0)

    # Load environment variables
    load_dotenv()
    google_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not google_key:
        logging.error("GOOGLE_PLACES_API_KEY not found in environment / .env file.")
        sys.exit(1)

    # ── Resolve location ──────────────────────
    lat, lng = None, None

    if args.latlng:
        try:
            lat, lng = map(float, args.latlng.split(","))
            logging.info(f"Using lat/lng: {lat}, {lng}")
        except ValueError:
            logging.error("--latlng must be in format 'lat,lng' e.g. '53.744,-2.011'")
            sys.exit(1)

    elif args.postcode:
        logging.info(f"Geocoding postcode: {args.postcode}")
        coords = geocode_postcode_nominatim(args.postcode)
        if not coords:
            # Fallback to Google Geocoding
            coords = geocode_location(args.postcode, google_key)
        if not coords:
            logging.error(f"Could not geocode postcode: {args.postcode}")
            sys.exit(1)
        lat, lng = coords
        logging.info(f"  → {lat}, {lng}")

    elif args.location:
        logging.info(f"Geocoding location: {args.location}")
        coords = geocode_location(args.location, google_key)
        if not coords:
            logging.error(f"Could not geocode location: {args.location}")
            sys.exit(1)
        lat, lng = coords
        logging.info(f"  → {lat}, {lng}")

    # ── Resolve categories ────────────────────
    if args.categories == "all":
        category_keys = list(MERIDIAN_CATEGORIES.keys())
    else:
        category_keys = [k.strip() for k in args.categories.split(",")]
        invalid = [k for k in category_keys if k not in MERIDIAN_CATEGORIES]
        if invalid:
            logging.error(f"Unknown category keys: {invalid}. Use --list-categories to see options.")
            sys.exit(1)

    logging.info(
        f"\n{'═'*52}\n"
        f"  Meridian Scraper\n"
        f"  Location : {lat:.4f}, {lng:.4f}\n"
        f"  Radius   : {args.radius}m\n"
        f"  Categories: {len(category_keys)} selected\n"
        f"  Max details: {args.max_details}\n"
        f"{'═'*52}"
    )

    # ── Run scrape ────────────────────────────
    records = run_scrape(
        lat=lat, lng=lng,
        radius=args.radius,
        category_keys=category_keys,
        api_key=google_key,
        max_details=args.max_details,
    )

    if not records:
        logging.info("No records collected. Exiting.")
        sys.exit(0)

    # ── Dry run ───────────────────────────────
    if args.dry_run:
        print(f"\n{'─'*52}")
        print(f"DRY RUN — {len(records)} records collected:\n")
        for r in records[:20]:
            print(f"  [{r['Category']}] {r['Name']} — {r['Address']}")
        if len(records) > 20:
            print(f"  … and {len(records) - 20} more")
        print()
        sys.exit(0)

    # ── Output ────────────────────────────────
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

    if args.output in ("csv", "both"):
        csv_path = args.csv_path or f"meridian_candidates_{timestamp}.csv"
        save_to_csv(records, csv_path)

    if args.output in ("airtable", "both"):
        at_key = os.getenv("AIRTABLE_API_KEY")
        at_base = os.getenv("AIRTABLE_BASE_ID")
        at_table = os.getenv("AIRTABLE_TABLE_NAME", "Candidates")
        if not at_key or not at_base:
            logging.error(
                "AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set in .env to push to Airtable."
            )
        else:
            push_to_airtable(records, at_key, at_base, at_table)

    logging.info("\n✓ Scrape complete.")

# ─────────────────────────────────────────────
# CSV → AIRTABLE PUSH
# Push an existing CSV file to Airtable.
# Useful for reviewing a CSV first, then pushing
# approved records without re-scraping.
#
# Usage:
#   python scrape_google.py --push-csv meridian_candidates_20260406.csv
# ─────────────────────────────────────────────

def load_csv(filepath: str) -> list[dict]:
    """Load records from a Meridian CSV file."""
    path = Path(filepath)
    if not path.exists():
        logging.error(f"CSV file not found: {filepath}")
        return []

    records = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Clean up numeric fields that CSV stores as strings
            for field in ["Google Rating", "Google Review Count",
                          "Latitude", "Longitude", "Distance (m)"]:
                val = row.get(field, "")
                if val == "":
                    continue
                try:
                    if field in ("Google Rating", "Latitude", "Longitude"):
                        row[field] = float(val)
                    else:
                        row[field] = int(float(val))
                except (ValueError, TypeError):
                    pass
            records.append(row)

    logging.info(f"  Loaded {len(records)} records from {filepath}")
    return records


def push_csv_to_airtable(filepath: str) -> None:
    """Load a CSV and push its contents to Airtable."""
    load_dotenv()
    at_key = os.getenv("AIRTABLE_API_KEY")
    at_base = os.getenv("AIRTABLE_BASE_ID")
    at_table = os.getenv("AIRTABLE_TABLE_NAME", "Candidates")

    if not at_key or not at_base:
        logging.error("AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set in .env")
        sys.exit(1)

    records = load_csv(filepath)
    if not records:
        logging.info("No records to push.")
        return

    push_to_airtable(records, at_key, at_base, at_table)

# ─────────────────────────────────────────────
# RESULTS CUTOFF
# Trim the final results list to a max count,
# prioritised by distance from search centre
# (closest first) then by Google rating.
# ─────────────────────────────────────────────

def apply_cutoff(records: list[dict], max_results: int) -> list[dict]:
    """
    Trim records to max_results, keeping the closest
    and highest-rated candidates first.
    """
    if not max_results or len(records) <= max_results:
        return records

    def sort_key(r):
        distance = r.get("Distance (m)", 999999)
        if distance == "":
            distance = 999999
        rating = r.get("Google Rating", 0)
        if rating == "":
            rating = 0
        # Sort by distance ascending, then rating descending
        return (int(distance), -float(rating))

    sorted_records = sorted(records, key=sort_key)
    trimmed = sorted_records[:max_results]

    logging.info(
        f"  Cutoff applied: kept {len(trimmed)} of {len(records)} records "
        f"(prioritised by proximity, then rating)"
    )
    return trimmed

def is_relevant(place: dict, details: dict, category_key: str) -> bool:
    """
    Check if a place is actually relevant to the Meridian category
    we were searching for. Google text search is very loose —
    this catches the worst mismatches.
    """
    cat = MERIDIAN_CATEGORIES.get(category_key, {})
    expected_types = set(cat.get("google_types", []))
    expected_keywords = [kw.lower() for kw in cat.get("keywords", [])]

    # Get all type and text signals from the place
    place_types = set(details.get("types") or place.get("types", []))
    name = (details.get("name") or place.get("name", "")).lower()
    editorial = details.get("editorial_summary", {}).get("overview", "").lower()

    # Check 1: Do any Google types overlap?
    type_match = bool(expected_types & place_types)

    # Check 2: Does the name or editorial summary contain any keywords?
    keyword_match = any(
        kw in name or kw in editorial
        for kw in expected_keywords
    )

    # Check 3: Reject obviously wrong types
    junk_types = {
        "real_estate_agency", "insurance_agency", "lawyer",
        "accounting", "lodging", "church", "local_government_office",
        "car_repair", "moving_company", "storage", "funeral_home",
        "travel_agency",
    }
    if place_types & junk_types and not type_match:
        return False

    return type_match or keyword_match


def main():
    args = parse_args()

    # Logging setup
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )

    # ── List categories mode ──────────────────
    if args.list_categories:
        print("\nMeridian Business Categories\n" + "─" * 40)
        for key, cat in MERIDIAN_CATEGORIES.items():
            print(f"  {key:<28} {cat['label']}")
        print()
        sys.exit(0)

    # ── Push CSV mode (no scraping, no location needed) ──
    if args.push_csv:
        logging.info(f"Pushing CSV to Airtable: {args.push_csv}")
        push_csv_to_airtable(args.push_csv)
        logging.info("\n✓ CSV push complete.")
        sys.exit(0)

    # Load environment variables
    load_dotenv()
    google_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not google_key:
        logging.error("GOOGLE_PLACES_API_KEY not found in environment / .env file.")
        sys.exit(1)

    # ── Resolve location ──────────────────────
    lat, lng = None, None

    if args.latlng:
        try:
            lat, lng = map(float, args.latlng.split(","))
            logging.info(f"Using lat/lng: {lat}, {lng}")
        except ValueError:
            logging.error("--latlng must be in format 'lat,lng' e.g. '53.744,-2.011'")
            sys.exit(1)

    elif args.postcode:
        logging.info(f"Geocoding postcode: {args.postcode}")
        coords = geocode_postcode_nominatim(args.postcode)
        if not coords:
            coords = geocode_location(args.postcode, google_key)
        if not coords:
            logging.error(f"Could not geocode postcode: {args.postcode}")
            sys.exit(1)
        lat, lng = coords
        logging.info(f"  → {lat}, {lng}")

    elif args.location:
        logging.info(f"Geocoding location: {args.location}")
        coords = geocode_location(args.location, google_key)
        if not coords:
            logging.error(f"Could not geocode location: {args.location}")
            sys.exit(1)
        lat, lng = coords
        logging.info(f"  → {lat}, {lng}")

    # ── Resolve categories ────────────────────
    if args.categories == "all":
        category_keys = list(MERIDIAN_CATEGORIES.keys())
    else:
        category_keys = [k.strip() for k in args.categories.split(",")]
        invalid = [k for k in category_keys if k not in MERIDIAN_CATEGORIES]
        if invalid:
            logging.error(f"Unknown category keys: {invalid}. Use --list-categories to see options.")
            sys.exit(1)

    logging.info(
        f"\n{'═'*52}\n"
        f"  Meridian Scraper\n"
        f"  Location : {lat:.4f}, {lng:.4f}\n"
        f"  Radius   : {args.radius}m\n"
        f"  Categories: {len(category_keys)} selected\n"
        f"  Max details: {args.max_details}\n"
        f"  Max results: {args.max_results or 'No limit'}\n"
        f"{'═'*52}"
    )

    # ── Run scrape ────────────────────────────
    records = run_scrape(
        lat=lat, lng=lng,
        radius=args.radius,
        category_keys=category_keys,
        api_key=google_key,
        max_details=args.max_details,
        max_results=args.max_results,
    )

    if not records:
        logging.info("No records collected. Exiting.")
        sys.exit(0)

    # ── Apply cutoff ──────────────────────────
    if args.max_results:
        records = apply_cutoff(records, args.max_results)

    # ── Dry run ───────────────────────────────
    if args.dry_run:
        print(f"\n{'─'*52}")
        print(f"DRY RUN — {len(records)} records:\n")
        for r in records[:20]:
            dist = r.get("Distance (m)", "?")
            rating = r.get("Google Rating", "—")
            print(f"  [{r['Category']}] {r['Name']} — {dist}m — ★{rating}")
        if len(records) > 20:
            print(f"  … and {len(records) - 20} more")
        print()
        sys.exit(0)

    # ── Output ────────────────────────────────
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M")

    if args.output in ("csv", "both"):
        csv_path = args.csv_path or f"meridian_candidates_{timestamp}.csv"
        save_to_csv(records, csv_path)

    if args.output in ("airtable", "both"):
        at_key = os.getenv("AIRTABLE_API_KEY")
        at_base = os.getenv("AIRTABLE_BASE_ID")
        at_table = os.getenv("AIRTABLE_TABLE_NAME", "Candidates")
        if not at_key or not at_base:
            logging.error(
                "AIRTABLE_API_KEY and AIRTABLE_BASE_ID must be set in .env to push to Airtable."
            )
        else:
            push_to_airtable(records, at_key, at_base, at_table)

    logging.info(f"\n✓ Scrape complete. {len(records)} records processed.")

if __name__ == "__main__":
    main()
