"""
airtable_to_supabase.py — Meridian Directory
==============================================
Transfers 'Published' business records from Airtable to Supabase.
This script acts as the 'Publish' stage in the Meridian system diagram.

It fetches records from the Airtable 'Candidates' table that have a 'Status'
of 'Published', transforms them into the Supabase 'listings' table schema,
and then upserts them to Supabase.

USAGE:
  python airtable_to_supabase.py

SETUP:
  pip install python-dotenv pyairtable supabase-py

  Ensure your .env file contains:
    AIRTABLE_API_KEY=your_airtable_api_key
    AIRTABLE_BASE_ID=your_airtable_base_id
    AIRTABLE_CANDIDATES_TABLE_NAME=Candidates # Or your actual table name

    SUPABASE_URL=your_supabase_project_url # e.g., https://xyz.supabase.co
    SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
    SUPABASE_LISTINGS_TABLE_NAME=listings # Or your actual table name
"""

import os
import sys
import json
import logging
import urllib.parse
from datetime import datetime, timezone

from dotenv import load_dotenv
from pyairtable import Api as AirtableApi
from supabase import create_client, Client

# --- Configuration ---
# Load environment variables
load_dotenv()

# Airtable
AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
AIRTABLE_CANDIDATES_TABLE_NAME = os.getenv("AIRTABLE_CANDIDATES_TABLE_NAME", "Candidates")

# Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
SUPABASE_LISTINGS_TABLE_NAME = os.getenv("SUPABASE_LISTINGS_TABLE_NAME", "listings")

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def get_airtable_client() -> AirtableApi:
    """Initializes and returns the Airtable API client."""
    if not AIRTABLE_API_KEY or not AIRTABLE_BASE_ID:
        logging.error("Airtable API key or Base ID not found in environment variables.")
        sys.exit(1)
    return AirtableApi(AIRTABLE_API_KEY)

def get_supabase_client() -> Client:
    """Initializes and returns the Supabase client."""
    if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
        logging.error("Supabase URL or Service Role Key not found in environment variables.")
        sys.exit(1)
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def fetch_approved_airtable_records(airtable_api: AirtableApi) -> list[dict]:
    """
    Fetches records from Airtable where the 'Status' field is 'Published'.
    Returns a list of dictionaries, where each dict is an Airtable record.
    """
    table = airtable_api.table(AIRTABLE_BASE_ID, AIRTABLE_CANDIDATES_TABLE_NAME)
    logging.info(f"Fetching 'Published' records from Airtable table: '{AIRTABLE_CANDIDATES_TABLE_NAME}'...")
    try:
        # Filter by Status = 'Published'
        records = table.all(formula="{Status} = 'Published'")
        logging.info(f"Found {len(records)} 'Published' records in Airtable.")
        return records
    except Exception as e:
        logging.error(f"Error fetching records from Airtable: {e}")
        return []

def transform_airtable_to_supabase_format(airtable_record: dict) -> dict:
    """
    Transforms a single Airtable record into the format expected by Supabase.
    Handles field renaming, type conversions, and default values.
    """
    fields = airtable_record.get("fields", {})
    
    current_time_utc = datetime.now(timezone.utc).isoformat()

    # Logic for Google Maps URL fallback
    google_maps_url = fields.get("google_maps_url")
    if not google_maps_url and fields.get("address"):
        encoded_address = urllib.parse.quote(fields.get("address"))
        google_maps_url = f"https://www.google.com/maps/search/?api=1&query={encoded_address}"

    supabase_data = {
        "name": fields.get("name"),
        "category": fields.get("category"),
        "category_key": fields.get("category_key"),
        "address": fields.get("address"),
        "latitude": fields.get("latitude"),
        "longitude": fields.get("longitude"),
        "phone": fields.get("phone"),
        "website": fields.get("website"),
        "email": fields.get("email"),
        "google_maps_url": google_maps_url,
        "photo_url": fields.get("photo_url"),
        "google_summary": fields.get("google_summary"),
        "opening_hours": fields.get("opening_hours"),
        "google_rating": fields.get("google_rating"),
        "google_review_count": fields.get("google_review_count"),
        "google_place_id": fields.get("google_place_id"),
        "source": fields.get("source"),
        "scrape_date": fields.get("scrape_date"),
        "status": "Published",
        "chain_flag": fields.get("chain_flag"),
        "editor_notes": fields.get("Editor Notes"),
        "story_draft": fields.get("Story Draft"),
        "description": fields.get("Story Draft") or fields.get("google_summary"), 
        "tags": fields.get("tags") or [],
        "is_featured": fields.get("is_featured") or False,
        "image_url": fields.get("image_url") or fields.get("photo_url"),
        "ranking_tier": fields.get("ranking_tier") or "standard",
        "category_slug": fields.get("category_slug"),
        "city_slug": fields.get("city_slug"),
        "area_slug": fields.get("area_slug"),
        "business_slug": fields.get("business_slug"),
        "social_facebook": fields.get("social_facebook"),
        "social_instagram": fields.get("social_instagram"),
        "social_twitter": fields.get("social_twitter"),
        "social_tiktok": fields.get("social_tiktok"),
        "social_linkedin": fields.get("social_linkedin"),
        "social_youtube": fields.get("social_youtube"),
        "synced_at": current_time_utc,
    }

    # Clean up None values for Supabase
    for key, value in supabase_data.items():
        if value is None or value == "":
            supabase_data[key] = None

    # Ensure numeric types are correct
    # Latitude and Longitude: double precision (float)
    for num_field in ["latitude", "longitude"]:
        val = supabase_data.get(num_field)
        if val is not None and isinstance(val, (str, float, int)):
            try:
                supabase_data[num_field] = float(val)
            except (ValueError, TypeError):
                supabase_data[num_field] = None

    # Google Rating: real (float)
    val = supabase_data.get("google_rating")
    if val is not None and isinstance(val, (str, float, int)):
        try:
            supabase_data["google_rating"] = float(val)
        except (ValueError, TypeError):
            supabase_data["google_rating"] = None

    # Google Review Count: integer
    val = supabase_data.get("google_review_count")
    if val is not None and isinstance(val, (str, float, int)):
        try:
            clean_val = str(val).replace(',', '').split('.')[0]
            supabase_data["google_review_count"] = int(clean_val) if clean_val else None
        except (ValueError, TypeError):
            supabase_data["google_review_count"] = None

    # Is Featured: boolean
    val = supabase_data.get("is_featured")
    if val is not None:
        if isinstance(val, bool):
            pass  # Already boolean
        elif isinstance(val, str):
            supabase_data["is_featured"] = val.lower() in ("true", "yes", "1")
        else:
            supabase_data["is_featured"] = bool(val)

    # Tags: text array
    val = supabase_data.get("tags")
    if val is not None:
        if isinstance(val, list):
            pass  # Already a list
        elif isinstance(val, str):
            # Try to parse as JSON array or comma-separated
            try:
                supabase_data["tags"] = json.loads(val)
            except (json.JSONDecodeError, ValueError):
                supabase_data["tags"] = [v.strip() for v in val.split(",") if v.strip()]
                if not supabase_data["tags"]:
                    supabase_data["tags"] = []
        else:
            supabase_data["tags"] = []

    # Supabase `scrape_date` is stored as text, validate it matches YYYY-MM-DD format
    if supabase_data.get("scrape_date"):
        try:
            datetime.strptime(supabase_data["scrape_date"], "%Y-%m-%d")
        except ValueError:
            logging.warning(f"Invalid scrape_date format for {supabase_data.get('name', 'Unknown Name')}: {supabase_data['scrape_date']}. Setting to None.")
            supabase_data["scrape_date"] = None

    return supabase_data

def upsert_to_supabase(supabase_client: Client, data_to_upsert: list[dict]) -> None:
    """
    Upserts a list of records to the Supabase 'listings' table.
    Uses 'google_place_id' as the unique identifier for conflict resolution.
    """
    if not data_to_upsert:
        logging.info("No data to upsert to Supabase.")
        return

    logging.info(f"Attempting to upsert {len(data_to_upsert)} records to Supabase table: '{SUPABASE_LISTINGS_TABLE_NAME}'...")
    
    try:
        response = supabase_client.table(SUPABASE_LISTINGS_TABLE_NAME).upsert(
            data_to_upsert,
            on_conflict="google_place_id"
        ).execute()
        
        if response.data:
            logging.info(f"Successfully upserted {len(response.data)} records to Supabase.")
        elif response.error:
            logging.error(f"Error upserting to Supabase: {response.error}")
        else:
            logging.warning("Upsert to Supabase completed, but response.data is empty.")

    except Exception as e:
        logging.error(f"An unexpected error occurred during Supabase upsert: {e}")

def main():
    airtable_api = get_airtable_client()
    supabase_client = get_supabase_client()

    airtable_records = fetch_approved_airtable_records(airtable_api)

    if not airtable_records:
        logging.info("No approved records found in Airtable. Exiting.")
        return

    supabase_records = []
    for record in airtable_records:
        transformed_record = transform_airtable_to_supabase_format(record)
        if transformed_record.get("google_place_id"):
            supabase_records.append(transformed_record)
        else:
            logging.warning(f"Skipping record due to missing 'Google Place ID': {record.get('fields', {}).get('Name', 'Unknown Name')}")

    if not supabase_records:
        logging.info("No valid records to push to Supabase. Exiting.")
        return

    upsert_to_supabase(supabase_client, supabase_records)
    logging.info("Airtable to Supabase sync process complete.")

if __name__ == "__main__":
    main()
