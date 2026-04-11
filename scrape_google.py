"""
scrape_google.py — Meridian Directory
======================================
Scrapes local business data from the Google Places API and writes
candidate records to Airtable (or a local CSV for review).

SETUP & USAGE
=============

1. ENVIRONMENT VARIABLES (add to .env file):
   - GOOGLE_PLACES_API_KEY: Your Google Places API key
   - AIRTABLE_API_KEY: Your Airtable token (optional, for direct push)
   - AIRTABLE_BASE_ID: Your Airtable base ID (optional, for direct push)
   - AIRTABLE_TABLE_NAME: Table name in Airtable (optional, defaults to "Candidates")

2. RUNNING THE SCRAPER:

   Basic usage (saves to CSV only):
   $ python scrape_google.py --location "BS5 0JS" --radius 500 --categories "food_produce"

   With result limits:
   $ python scrape_google.py -l "BS5 0JS" -r 500 -c "food_produce" \
     --max-results 100 --max-details 100

   Push directly to Airtable:
   $ python scrape_google.py -l "BS5 0JS" -r 500 -c "food_produce" --output airtable

   Save CSV AND push to Airtable:
   $ python scrape_google.py -l "BS5 0JS" -r 500 -c "food_produce" --output both

   Push existing CSV to Airtable (no scraping):
   $ python scrape_google.py --load-csv meridian_candidates_2026-04-11_161941.csv

3. CSV TO AIRTABLE (Manual Import):

   If you have a CSV and want to import manually:
   a) Ensure Airtable table has these fields (case-sensitive):
      - name, category, category_key, category_slug, address
      - city_slug, area_slug, business_slug
      - latitude, longitude, phone, website, email
      - google_maps_url, photo_url, image_url
      - google_summary, opening_hours
      - google_rating, google_review_count, google_place_id, tags
      - chain_flag, social_facebook, social_instagram, social_twitter,
        social_tiktok, social_linkedin, social_youtube
      - status, ranking_tier, source, scrape_date

   b) In Airtable: Grid view → + (add) → "Import data" → CSV
   c) Match columns to fields in Airtable
   d) Set google_place_id as primary key/unique identifier to avoid duplicates

4. AVAILABLE CATEGORIES:
   - food_produce: Food shops, bakeries, markets
   - restaurants_cafes: Restaurants and cafés
   - drinks_brewing: Breweries, bars, wineries
   - craft_makers: Ceramics, jewelry, woodworking, etc.
   - art_design: Art galleries, artists, designers
   - home_interiors: Furniture, interior design
   - plants_garden: Florists, garden centers
   - health_wellbeing: Spas, massage, wellness
"""

import os
import sys
import csv
import time
import json
import argparse
import logging
import re
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
# KNOWN RETAIL CHAINS (to be tagged as chain_flag)
# ─────────────────────────────────────────────
KNOWN_CHAINS = {
    # Supermarkets
    "Iceland", "Tesco", "Sainsbury's", "Asda", "Morrisons", "Waitrose", "M&S Food Hall",
    "Budgens", "Co-op", "Lidl", "Aldi", "Marks & Spencer", "Ocado",
    # Other retail
    "Poundland", "Home Bargains", "B&M", "The Range",
}

# ─────────────────────────────────────────────
# MERIDIAN BUSINESS CATEGORIES
# ─────────────────────────────────────────────
MERIDIAN_CATEGORIES = {
    # Food & Drink
    "food_produce": {
        "label": "Food & Produce",
        "slug": "food-and-produce",
        "google_types": ["bakery", "butcher", "supermarket", "grocery_or_supermarket"],
        "keywords": [
            "farm shop", "deli", "delicatessen", "fishmonger", "greengrocer", "cheese", "charcuterie", "market stall", 
            "farmers market", "food market", "sweet mart", "sweet shop", "confectionery", "grocery", "supermarket",
            "independent grocer", "local market"
        ],
    },
    "restaurants_cafes": {
        "label": "Restaurants & Cafés",
        "slug": "restaurants-and-cafes",
        "google_types": ["restaurant", "cafe"],
        "keywords": ["supper club", "pop-up restaurant", "street food", "bistro", "brasserie", "gastropub"],
    },
    "drinks_brewing": {
        "label": "Drinks & Brewing",
        "slug": "drinks-and-brewing",
        "google_types": ["bar", "liquor_store"],
        "keywords": ["brewery", "microbrewery", "distillery", "gin", "cider", "winery", "wine merchant", "craft beer", "kombucha"],
    },
    # Craft & Making
    "craft_makers": {
        "label": "Craft & Makers",
        "slug": "craft-and-makers",
        "google_types": ["art_gallery"],
        "keywords": ["ceramics studio", "pottery", "woodworker", "blacksmith", "jeweller", "jewellery maker", "silversmith", "weaver", "glassblower", "printmaker", "leather craftsman", "bookbinder"],
    },
    "art_design": {
        "label": "Art & Design",
        "slug": "art-and-design",
        "google_types": ["art_gallery", "painter"],
        "keywords": ["artist", "illustrator", "graphic designer", "sculptor", "photographer", "printmaker", "muralist", "studio"],
    },
    # Home & Garden
    "home_interiors": {
        "label": "Home & Interiors",
        "slug": "home-and-interiors",
        "google_types": ["furniture_store", "home_goods_store", "interior_designer"],
        "keywords": ["interior design", "upholstery", "antiques", "vintage furniture", "restoration", "cabinet maker"],
    },
    "plants_garden": {
        "label": "Plants & Garden",
        "slug": "plants-and-garden",
        "google_types": ["florist", "garden_center", "landscaping"],
        "keywords": ["nursery", "horticulture", "landscape gardener", "garden design", "wildflower", "allotment"],
    },
    # Wellbeing & Care
    "health_wellbeing": {
        "label": "Health & Wellbeing",
        "slug": "health-and-wellbeing",
        "google_types": ["physiotherapist", "gym", "spa", "beauty_salon"],
        "keywords": ["osteopath", "acupuncture", "massage therapist", "yoga teacher", "pilates", "nutritionist", "herbalist", "naturopath"],
    },
}

# ─────────────────────────────────────────────
# HELPERS & SCRAPING LOGIC
# ─────────────────────────────────────────────

def slugify(text: str) -> str:
    """Convert text to URL-safe slug format.
    Removes apostrophes, special characters, and converts spaces to hyphens.
    """
    if not text: return ""
    # Remove apostrophes and other problematic characters
    text = text.replace("'", "").replace('"', "")  # Remove quotes
    # Replace spaces, ampersands, and slashes with hyphens
    text = re.sub(r'[\s&/]+', '-', text.lower())
    # Remove any other special characters except hyphens
    text = re.sub(r'[^a-z0-9-]', '', text)
    # Clean up multiple consecutive hyphens
    text = re.sub(r'-+', '-', text)
    return text.strip('-')

# Generic/irrelevant types to EXCLUDE from results
EXCLUDED_TYPES = {
    "administrative_area_level_1", "administrative_area_level_2", "administrative_area_level_3",
    "country", "locality", "postal_code", "postal_town", "intersection", "colloquial_area",
    "point_of_interest", "establishment", "place_of_worship", "church", "mosque", "synagogue",
    "gym", "health", "hospital", "medical_clinic", "pharmacy", "dentist",
    "school", "university", "library", "civic_center",
    "lawyer", "accounting", "insurance_agency",
    "car_rental", "gas_station", "parking", "auto_repair", "tire_store",
    "real_estate_agency", "storage",
}

def is_chain_business(name: str) -> bool:
    """Check if business name contains a known chain indicator."""
    name_upper = name.upper()
    for chain in KNOWN_CHAINS:
        if chain.upper() in name_upper:
            return True
    return False

# Types/keywords that are EXPLICITLY INCORRECT for this category
BAD_FOOD_TYPES = {
    "gym", "health", "hospital", "medical_clinic", "pharmacy", "dentist", "veterinary_care",
    "car_rental", "gas_station", "parking", "auto_repair", "tire_store", "car_wash",
    "real_estate_agency", "lawyer", "accounting", "insurance_agency", "bank", "book_store",
    "bowling_alley", "amusement_park", "movie_theater", "nightclub",
}

BAD_FOOD_KEYWORDS = {
    "gym", "boxing", "yoga", "fitness", "wellness center", "clinic", "pharmacy", "dentist",
    "lawyer", "accountant", "real estate", "debt collection", "garage", "tire", "auto",
    "church", "mosque", "synagogue", "temple", "ministry", "tabernacle",
}

def is_relevant_place(details: dict, meridian_category: str) -> bool:
    """Permissive filtering - only rejects obviously wrong categories.
    Trust that most API results are at least in the ballpark.
    Final filtering happens in Airtable curation.
    """
    place_types = set(details.get("types", []))
    place_name = details.get("name", "").lower()
    
    # ALWAYS REJECT: Purely administrative/generic areas
    if place_types.issubset({"administrative_area_level_1", "administrative_area_level_2", 
                             "administrative_area_level_3", "country", "locality", "postal_code", 
                             "postal_town", "colloquial_area"}):
        return False
    
    # ALWAYS REJECT: Non-food categories in FOOD search
    if meridian_category in ["food_produce", "restaurants_cafes", "drinks_brewing"]:
        # Reject if name clearly indicates it's NOT a food business
        if any(bad in place_name for bad in BAD_FOOD_KEYWORDS):
            return False
        
        # Reject if types are ONLY bad types (has gym but no food, for example)
        if place_types.intersection(BAD_FOOD_TYPES):
            # Only reject if it has NO food-related types
            food_types = {"bakery", "butcher", "grocery_or_supermarket", "food", "meal_takeaway",
                         "cafe", "restaurant", "bar", "liquor_store", "supermarket", "market", "store"}
            if not place_types.intersection(food_types):
                return False
    
    # For craft/art/other categories, be similarly permissive
    # Let curator decide on edge cases
    
    # DEFAULT: Accept and let curator decide
    return True

def extract_social_and_email(website_url: str) -> dict:
    """
    Crawls the homepage of the given website to find social links and emails.
    """
    socials = {
        "Email": "",
        "Social Facebook": "",
        "Social Instagram": "",
        "Social Twitter": "",
        "Social Tiktok": "",
        "Social Linkedin": "",
        "Social Youtube": "",
    }
    if not website_url:
        return socials

    try:
        logging.info(f"    Scraping website for socials: {website_url}")
        resp = requests.get(website_url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return socials
        
        html = resp.text
        
        # Regex Patterns
        patterns = {
            "Email": r'mailto:([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            "Social Facebook": r'https?://(?:www\.)?facebook\.com/[a-zA-Z0-9._-]+',
            "Social Instagram": r'https?://(?:www\.)?instagram\.com/[a-zA-Z0-9._-]+',
            "Social Twitter": r'https?://(?:www\.)?(?:twitter\.com|x\.com)/[a-zA-Z0-9._-]+',
            "Social Tiktok": r'https?://(?:www\.)?tiktok\.com/@[a-zA-Z0-9._-]+',
            "Social Linkedin": r'https?://(?:www\.)?linkedin\.com/(?:company|in)/[a-zA-Z0-9._-]+',
            "Social Youtube": r'https?://(?:www\.)?youtube\.com/(?:c/|channel/|user/)[a-zA-Z0-9._-]+',
        }

        for key, pattern in patterns.items():
            match = re.search(pattern, html)
            if match:
                socials[key] = match.group(1) if key == "Email" else match.group(0)

    except Exception as e:
        logging.warning(f"    Failed to scrape website {website_url}: {e}")
    
    return socials

PLACES_NEARBY_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
PLACES_DETAILS_URL = "https://maps.googleapis.com/maps/api/place/details/json"
PLACES_TEXT_URL = "https://maps.googleapis.com/maps/api/place/textsearch/json"
GEOCODE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

DETAIL_FIELDS = ",".join([
    "place_id", "name", "formatted_address", "formatted_phone_number",
    "website", "url", "opening_hours", "photos", "geometry",
    "rating", "user_ratings_total", "business_status", "types",
    "editorial_summary", "address_components"
])

def geocode_location(query: str, api_key: str) -> tuple[float, float] | None:
    resp = requests.get(GEOCODE_URL, params={"address": query, "key": api_key}, timeout=10)
    data = resp.json()
    if data.get("status") == "OK":
        loc = data["results"][0]["geometry"]["location"]
        return loc["lat"], loc["lng"]
    return None

def geocode_postcode_nominatim(postcode: str) -> tuple[float, float] | None:
    geolocator = Nominatim(user_agent="meridian-scraper")
    try:
        location = geolocator.geocode(postcode, country_codes="GB", timeout=10)
        if location:
            return location.latitude, location.longitude
    except:
        pass
    return None

def nearby_search(lat: float, lng: float, radius: int, place_type: str, api_key: str) -> list[dict]:
    results = []
    params = {"location": f"{lat},{lng}", "radius": radius, "type": place_type, "key": api_key}
    page = 0
    while page < 3:
        resp = requests.get(PLACES_NEARBY_URL, params=params, timeout=10)
        data = resp.json()
        if data.get("status") not in ("OK", "ZERO_RESULTS"): break
        results.extend(data.get("results", []))
        next_token = data.get("next_page_token")
        if not next_token: break
        time.sleep(2)
        params = {"pagetoken": next_token, "key": api_key}
        page += 1
    return results

def text_search(lat: float, lng: float, radius: int, keyword: str, api_key: str) -> list[dict]:
    results = []
    params = {"query": keyword, "location": f"{lat},{lng}", "radius": radius, "key": api_key}
    resp = requests.get(PLACES_TEXT_URL, params=params, timeout=10)
    data = resp.json()
    if data.get("status") == "OK":
        results.extend(data.get("results", []))
    return results

def get_place_details(place_id: str, api_key: str) -> dict:
    params = {"place_id": place_id, "fields": DETAIL_FIELDS, "key": api_key}
    resp = requests.get(PLACES_DETAILS_URL, params=params, timeout=10)
    data = resp.json()
    return data.get("result", {}) if data.get("status") == "OK" else {}

def normalise(place: dict, details: dict, meridian_category: str, api_key: str) -> dict:
    name = details.get("name") or place.get("name", "")
    address = details.get("formatted_address") or place.get("vicinity", "")
    website = details.get("website", "")
    
    # Skip if not operational
    if details.get("business_status") != "OPERATIONAL":
        logging.debug(f"Skipping {name}: business_status = {details.get('business_status')}")
        return None
    
    # Detect if this is a chain business
    is_chain = is_chain_business(name)
    chain_flag = "chain" if is_chain else "independent"
    
    # Extract slugs from address components
    components = details.get("address_components", [])
    city = next((c["long_name"] for c in components if "postal_town" in c["types"]), "")
    area = next((c["long_name"] for c in components if "neighborhood" in c["types"] or "sublocality" in c["types"]), "")
    
    # Fallback: if city not found, try to extract from full address
    if not city:
        addr_parts = address.split(",")
        if len(addr_parts) >= 3:
            # Typically format is: street, area, city, postcode
            city = addr_parts[-2].strip()
        elif len(addr_parts) >= 2:
            city = addr_parts[-1].strip()
    
    # Fallback: if area not found, try to extract from address
    if not area:
        addr_parts = address.split(",")
        if len(addr_parts) >= 2:
            area = addr_parts[0].strip()
    
    # Scrape website for socials/email
    social_data = extract_social_and_email(website)

    # Photos
    photos = details.get("photos") or place.get("photos", [])
    photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photo_reference={photos[0].get('photo_reference')}&key={api_key}" if photos else ""

    cat_config = MERIDIAN_CATEGORIES.get(meridian_category, {})
    
    # Format tags as a PostgreSQL array string representation
    tags = details.get("types", [])
    tags_str = "{" + ",".join(f'"{t}"' for t in tags) + "}" if tags else "{}"
    
    # Determine ranking tier based on chain status
    ranking_tier = "standard" if not is_chain else "low"
    
    return {
        "name": name,
        "category": cat_config.get("label", meridian_category),
        "category_key": meridian_category,
        "category_slug": cat_config.get("slug", slugify(meridian_category)),
        "address": address,
        "city_slug": slugify(city),
        "area_slug": slugify(area),
        "business_slug": slugify(name),
        "latitude": (details.get("geometry") or place.get("geometry", {})).get("location", {}).get("lat"),
        "longitude": (details.get("geometry") or place.get("geometry", {})).get("location", {}).get("lng"),
        "phone": details.get("formatted_phone_number", ""),
        "website": website,
        "email": social_data["Email"],
        "google_maps_url": details.get("url", ""),
        "photo_url": photo_url,
        "image_url": photo_url,
        "google_summary": details.get("editorial_summary", {}).get("overview", ""),
        "opening_hours": " | ".join(details.get("opening_hours", {}).get("weekday_text", [])),
        "google_rating": details.get("rating"),
        "google_review_count": details.get("user_ratings_total"),
        "google_place_id": details.get("place_id") or place.get("place_id", ""),
        "tags": tags_str,
        "chain_flag": chain_flag,
        "social_facebook": social_data["Social Facebook"],
        "social_instagram": social_data["Social Instagram"],
        "social_twitter": social_data["Social Twitter"],
        "social_tiktok": social_data["Social Tiktok"],
        "social_linkedin": social_data["Social Linkedin"],
        "social_youtube": social_data["Social Youtube"],
        "status": "pending",
        "ranking_tier": ranking_tier,
        "source": "Google Places",
        "scrape_date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "last_synced_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S"),
    }

def list_airtable_fields(api_key: str, base_id: str, table_name: str) -> None:
    """List all field names in the Airtable table (for debugging)."""
    if not AIRTABLE_AVAILABLE:
        logging.error("Airtable not installed. Install with: pip install pyairtable")
        return
    
    try:
        api = AirtableApi(api_key)
        table = api.table(base_id, table_name)
        schema = table.schema()
        # Get field names from schema
        field_names = [field.name for field in schema.fields]
        
        logging.info(f"Fields in Airtable table '{table_name}':")
        for fname in sorted(field_names):
            logging.info(f"  - {fname}")
    except Exception as e:
        logging.error(f"Failed to list Airtable fields: {e}")

def load_csv_and_push(csv_filepath: str, api_key: str, base_id: str, table_name: str) -> None:
    """Load an existing CSV and push to Airtable without scraping.
    
    Automatically maps CSV column names to Airtable field names.
    """
    if not AIRTABLE_AVAILABLE:
        logging.error("Airtable not installed. Install with: pip install pyairtable")
        return
    
    if not os.path.exists(csv_filepath):
        logging.error(f"CSV file not found: {csv_filepath}")
        return
    
    # Get column mapping for field name translation
    mapping = get_column_mapping()
    
    records = []
    try:
        with open(csv_filepath, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Rename columns according to mapping
                mapped_row = {}
                for csv_col, at_field in mapping.items():
                    if csv_col in row and row[csv_col]:
                        mapped_row[at_field] = row[csv_col]
                # Always include google_place_id as key field, even if other fields are empty
                if "google_place_id" in row:
                    mapped_row["google_place_id"] = row["google_place_id"]
                if mapped_row:  # Only add non-empty rows
                    records.append(mapped_row)
        logging.info(f"Loaded {len(records)} records from {csv_filepath}")
    except Exception as e:
        logging.error(f"Failed to read CSV: {e}")
        return
    
    if not records:
        logging.info("No records in CSV.")
        return
    
    logging.info(f"Pushing {len(records)} records to Airtable...")
    push_to_airtable(records, api_key, base_id, table_name)
    logging.info("Done!")

def get_column_mapping() -> dict:
    """Return the CSV to Airtable field name mapping (snake_case)."""
    return {
        "name": "name",
        "category": "category",
        "category_key": "category_key",
        "category_slug": "category_slug",
        "address": "address",
        "city_slug": "city_slug",
        "area_slug": "area_slug",
        "business_slug": "business_slug",
        "latitude": "latitude",
        "longitude": "longitude",
        "phone": "phone",
        "website": "website",
        "email": "email",
        "google_maps_url": "google_maps_url",
        "photo_url": "photo_url",
        "image_url": "image_url",
        "google_summary": "google_summary",
        "opening_hours": "opening_hours",
        "google_rating": "google_rating",
        "google_review_count": "google_review_count",
        "google_place_id": "google_place_id",
        "tags": "tags",
        "chain_flag": "chain_flag",
        "social_facebook": "social_facebook",
        "social_instagram": "social_instagram",
        "social_twitter": "social_twitter",
        "social_tiktok": "social_tiktok",
        "social_linkedin": "social_linkedin",
        "social_youtube": "social_youtube",
        "status": "status",
        "ranking_tier": "ranking_tier",
        "source": "source",
        "scrape_date": "scrape_date",
        "last_synced_at": "last_synced_at",
    }

def get_valid_airtable_fields(api_key: str, base_id: str, table_name: str) -> set:
    """Get the set of valid field names from Airtable table schema."""
    if not AIRTABLE_AVAILABLE:
        return set()
    
    try:
        api = AirtableApi(api_key)
        table = api.table(base_id, table_name)
        schema = table.schema()
        field_names = {field.name for field in schema.fields}
        logging.debug(f"Found {len(field_names)} fields in Airtable")
        return field_names
    except Exception as e:
        logging.error(f"Failed to get Airtable schema: {e}")
        return set()

def push_to_airtable(records: list[dict], api_key: str, base_id: str, table_name: str) -> None:
    if not AIRTABLE_AVAILABLE: return
    try:
        api = AirtableApi(api_key)
        table = api.table(base_id, table_name)
        
        # Get valid field names from Airtable schema
        valid_fields = get_valid_airtable_fields(api_key, base_id, table_name)
        if not valid_fields:
            logging.error("Could not determine valid fields. Aborting push.")
            return
        
        # Get column mapping for field name translation
        mapping = get_column_mapping()
        
        formatted = []
        for r in records:
            # Map CSV column names to Airtable field names
            mapped_record = {}
            for csv_col, airtable_field in mapping.items():
                # Only include fields that exist in Airtable
                if airtable_field in valid_fields and csv_col in r and r[csv_col] not in (None, ""):
                    mapped_record[airtable_field] = r[csv_col]
            # Always include google_place_id as key field if it exists in Airtable
            if "google_place_id" in valid_fields and "google_place_id" in r:
                mapped_record["google_place_id"] = r["google_place_id"]
            if mapped_record:
                formatted.append({"fields": mapped_record})

        if not formatted:
            logging.warning("No valid records to push after filtering to available fields.")
            logging.info(f"Available fields in Airtable: {sorted(valid_fields)}")
            return
        
        logging.info(f"Pushing {len(formatted)} records with {len(valid_fields)} available fields...")
        for i in range(0, len(formatted), 10):
            try:
                table.batch_upsert(formatted[i:i+10], key_fields=["google_place_id"], typecast=True)
                logging.debug(f"Successfully upserted batch {i//10 + 1}")
                time.sleep(0.25)
            except Exception as e:
                logging.error(f"Failed to upsert batch: {e}")
                continue
    except Exception as e:
        logging.error(f"Airtable connection failed, skipping push: {e}")

def save_to_csv(records: list[dict], filepath: str) -> None:
    if not records: return
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

def run_scrape(lat, lng, radius, category_keys, api_key, max_details=200, max_results=None, distance_filter_metres=None):
    all_places = {}
    for cat_key in category_keys:
        cat = MERIDIAN_CATEGORIES.get(cat_key)
        if not cat: continue
        logging.info(f"Scraping category: {cat['label']}")
        
        # PRIORITIZE: Text search by keywords first (finds specific local places)
        for kw in cat["keywords"]:
            for p in text_search(lat, lng, radius, kw, api_key):
                all_places[p["place_id"]] = (p, cat_key)
        
        # THEN: Nearby search by type (finds general business types)
        for gtype in cat["google_types"]:
            for p in nearby_search(lat, lng, radius, gtype, api_key):
                all_places[p["place_id"]] = (p, cat_key)

    results = []
    details_count = 0
    for pid, (place, cat_key) in all_places.items():
        if details_count >= max_details: 
            logging.info(f"Reached max details limit: {max_details}")
            break
        if max_results and len(results) >= max_results:
            logging.info(f"Reached max results limit: {max_results}")
            break

        logging.info(f"Fetching details for: {place.get('name')}")
        details = get_place_details(pid, api_key)
        
        # Post-filter by distance if specified
        if distance_filter_metres:
            result_lat = (details.get("geometry") or place.get("geometry", {})).get("location", {}).get("lat")
            result_lng = (details.get("geometry") or place.get("geometry", {})).get("location", {}).get("lng")
            if result_lat and result_lng:
                dist = haversine_metres(lat, lng, result_lat, result_lng)
                if dist > distance_filter_metres:
                    logging.debug(f"Skipping {details.get('name')}: {dist}m > {distance_filter_metres}m filter")
                    continue
        
        # Check relevance before normalizing
        if not is_relevant_place(details, cat_key):
            logging.debug(f"Skipping {details.get('name')}: not relevant for category {cat_key}")
            continue
        
        normalized = normalise(place, details, cat_key, api_key)
        
        # Skip if normalise returned None (e.g., not operational)
        if normalized:
            results.append(normalized)
        
        details_count += 1
        time.sleep(0.1)
    return results

def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description="Meridian Google Scraper")
    
    # Location
    parser.add_argument("--location", "-l", help="Place name or postcode")
    parser.add_argument("--radius", "-r", type=int, default=2000, help="Search radius in meters")
    
    # Filtering
    parser.add_argument("--categories", "-c", default="all", help="Comma-separated category keys or 'all'")
    
    # Limits
    parser.add_argument("--max-details", type=int, default=200, help="Max Details API calls")
    parser.add_argument("--max-results", type=int, default=None, help="Max results to keep")
    
    # Distance filtering
    parser.add_argument("--distance-filter", type=int, default=None, help="Post-filter results within N metres of search location (e.g., 500 for 500m)")
    
    # CSV Loading (for pushing existing CSV without scraping)
    parser.add_argument("--load-csv", help="Load and push existing CSV to Airtable (skip scraping)")
    
    # Airtable diagnostics
    parser.add_argument("--list-airtable-fields", action="store_true", help="List all field names in the Airtable table")
    
    # Output
    parser.add_argument("--output", "-o", choices=["airtable", "csv", "both"], default="both")
    parser.add_argument("--verbose", "-v", action="store_true")

    args = parser.parse_args()
    
    # Logging setup
    logging.basicConfig(level=logging.DEBUG if args.verbose else logging.INFO, format="%(message)s")

    # Airtable credentials (needed for any Airtable operation)
    at_key = os.getenv("AIRTABLE_API_KEY")
    at_base = os.getenv("AIRTABLE_BASE_ID")
    at_table = os.getenv("AIRTABLE_TABLE_NAME", "Candidates")

    # If --list-airtable-fields is provided, show field names and exit
    if args.list_airtable_fields:
        if not at_key or not at_base:
            logging.error("Airtable credentials not set. Set AIRTABLE_API_KEY and AIRTABLE_BASE_ID in .env")
            return
        list_airtable_fields(at_key, at_base, at_table)
        return

    # If --load-csv is provided, just load and push (skip scraping)
    if args.load_csv:
        if not at_key or not at_base:
            logging.error("Airtable credentials not set. Set AIRTABLE_API_KEY and AIRTABLE_BASE_ID in .env")
            return
        load_csv_and_push(args.load_csv, at_key, at_base, at_table)
        return

    # Otherwise, do scraping
    google_key = os.getenv("GOOGLE_PLACES_API_KEY")
    if not google_key:
        logging.error("GOOGLE_PLACES_API_KEY not found.")
        return

    # Geocode
    coords = geocode_location(args.location, google_key) if args.location else None
    if not coords:
        logging.error(f"Could not geocode location: {args.location}")
        return

    # Categories
    if args.categories == "all":
        category_keys = list(MERIDIAN_CATEGORIES.keys())
    else:
        category_keys = [k.strip() for k in args.categories.split(",")]

    # Run Scrape
    records = run_scrape(
        lat=coords[0], 
        lng=coords[1], 
        radius=args.radius, 
        category_keys=category_keys, 
        api_key=google_key, 
        max_details=args.max_details,
        max_results=args.max_results,
        distance_filter_metres=args.distance_filter
    )
    
    if not records:
        logging.info("No records found.")
        return

    # Output handling: ALWAYS save CSV first (safety backup)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    csv_filepath = f"meridian_candidates_{timestamp}.csv"
    save_to_csv(records, csv_filepath)
    logging.info(f"✓ Data saved to {csv_filepath}")
    
    # Then push to Airtable if requested
    if args.output in ("airtable", "both"):
        if at_key and at_base:
            logging.info(f"Pushing {len(records)} records to Airtable...")
            push_to_airtable(records, at_key, at_base, at_table)
        else:
            logging.warning("Airtable credentials not set. Data saved to CSV but not pushed to Airtable.")

    logging.info(f"Done. Processed {len(records)} records.")

if __name__ == "__main__":
    main()
