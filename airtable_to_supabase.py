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
import logging
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

    supabase_data = {
        "name": fields.get("Name"),
        "category": fields.get("Category"),
        "category_key": fields.get("Category Key"),
        "address": fields.get("Address"),
        "latitude": fields.get("Latitude"),
        "longitude": fields.get("Longitude"),
        "phone": fields.get("Phone"),
        "website": fields.get("Website"),
        "google_maps_url": fields.get("Google Maps URL"),
        "photo_url": fields.get("Photo URL (raw)"),
        "google_summary": fields.get("Google Summary"),
        "opening_hours": fields.get("Opening Hours"),
        "google_rating": fields.get("Google Rating"),
        "google_review_count": fields.get("Google Review Count"),
        "google_place_id": fields.get("Google Place ID"), # This will be our unique identifier
        "source": fields.get("Source"),
        "scrape_date": fields.get("Scrape Date"), # YYYY-MM-DD string
        "status": "Published", # Explicitly set status for Supabase
        "chain_flag": fields.get("Chain Flag"),
        "editor_notes": fields.get("Editor Notes"),
        "story_draft": fields.get("Story Draft"),
        "description": fields.get("Description") or fields.get("Story Draft") or fields.get("Google Summary"), 
        "tags": [], # For MVP, start with empty list. Could derive from category_key later.
        "is_featured": False, # Default to False for MVP
        "image_url": fields.get("Image URL") or fields.get("Photo URL (raw)"),
        "synced_at": current_time_utc, # Timestamp of when it was synced to Supabase
    }

    # Clean up None values for Supabase, especially for numeric fields
    for key, value in supabase_data.items():
        if value is None or value == "":
            supabase_data[key] = None # Supabase prefers None for nulls

    # Ensure numeric types are correct (Airtable might return them as strings)
    for num_field in ["latitude", "longitude", "google_rating", "google_review_count"]:
        val = supabase_data.get(num_field)
        if isinstance(val, str):
            try:
                if num_field == "google_review_count":
                    # Strip commas and handle decimals that might be in a string
                    clean_val = val.replace(',', '').split('.')[0]
                    supabase_data[num_field] = int(clean_val) if clean_val else None
                else:
                    supabase_data[num_field] = float(val)
            except (ValueError, TypeError):
                supabase_data[num_field] = None

    # Supabase `date` type expects 'YYYY-MM-DD'
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
            logging.warning("Upsert to Supabase completed, but response.data is empty and no error reported. Check Supabase logs.")

    except Exception as e:
        logging.error(f"An unexpected error occurred during Supabase upsert: {e}")

def main():
    airtable_api = get_airtable_client()
    supabase_client = get_supabase_client()

    airtable_records = fetch_approved_airtable_records(airtable_api)

    if not airtable_records:
        logging.info("No approved records found in Airtable to sync to Supabase. Exiting.")
        return

    supabase_records = []
    for record in airtable_records:
        transformed_record = transform_airtable_to_supabase_format(record)
        # Only add if it has a Google Place ID, which is our unique key for upserting
        if transformed_record.get("google_place_id"):
            supabase_records.append(transformed_record)
        else:
            logging.warning(f"Skipping record due to missing 'Google Place ID': {record.get('fields', {}).get('Name', 'Unknown Name')}")

    if not supabase_records:
        logging.info("No valid records to push to Supabase after transformation. Exiting.")
        return

    upsert_to_supabase(supabase_client, supabase_records)
    logging.info("Airtable to Supabase sync process complete.")

if __name__ == "__main__":
    main()