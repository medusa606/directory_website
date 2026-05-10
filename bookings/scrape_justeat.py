"""
Just Eat UK restaurant scraper — postcode API approach.

Strategy:
  1. Read unique postcodes from bookings/listings.csv
  2. For each postcode, call the Just Eat public enriched-restaurant API:
       https://api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}
  3. Parse JSON response, deduplicate by restaurant uniqueName
  4. Save incrementally to bookings/justeat.csv

Note: The API returns restaurants that deliver to a given postcode, so there
will be overlap across postcodes. Deduplication is done on `uniqueName`.

Output CSV columns:
  service, name, address, postcode, url, cuisines

Usage:
  python bookings/scrape_justeat.py
  python bookings/scrape_justeat.py --postcode BS1 --postcode BS6
  python bookings/scrape_justeat.py --limit 5
"""

import os
import csv
import time
import re
import argparse
import requests

# ── Constants ────────────────────────────────────────────────────────────────

LISTINGS_CSV = 'bookings/listings.csv'
OUTPUT_CSV = 'bookings/justeat.csv'
CHECKPOINT_EVERY = 10   # postcodes processed before checkpoint save
REQUEST_DELAY = 2.0
BACKOFF_BASE = 10
MAX_RETRIES = 5

API_URL = 'https://api.just-eat.io/discovery/uk/restaurants/enriched/bypostcode/{postcode}'

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept': 'application/json',
    'Accept-Language': 'en-GB,en;q=0.9',
}

FIELDNAMES = ['service', 'name', 'address', 'postcode', 'url', 'cuisines']

UK_POSTCODE_RE = re.compile(
    r'\b([A-Z]{1,2}[0-9][0-9A-Z]?\s*[0-9][A-Z]{2})\b', re.IGNORECASE
)


# ── Postcode helpers ──────────────────────────────────────────────────────────

def _normalise_postcode(value):
    return re.sub(r'\s+', '', str(value).upper().strip())


def _extract_postcode(text):
    m = UK_POSTCODE_RE.search(str(text).upper())
    return _normalise_postcode(m.group(1)) if m else ''


def _read_postcodes_from_listings(listings_csv):
    """Return sorted list of unique normalised UK postcodes from the listings CSV."""
    postcodes = set()
    if not os.path.exists(listings_csv):
        print(f'  ⚠ Listings CSV not found: {listings_csv}')
        return []
    with open(listings_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            address = row.get('address', '')
            pc = _extract_postcode(address)
            if pc:
                postcodes.add(pc)
    return sorted(postcodes)


# ── HTTP helper ───────────────────────────────────────────────────────────────

def _get_json(session, postcode):
    url = API_URL.format(postcode=postcode)
    wait = BACKOFF_BASE
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code in (429, 503, 504):
                print(f'  ⚠ HTTP {resp.status_code} on attempt {attempt}, waiting {wait}s…')
                time.sleep(wait)
                wait = min(wait * 2, 160)
                continue
            if resp.status_code == 404:
                # No restaurants found for this postcode
                return {'restaurants': []}
            print(f'  ✗ HTTP {resp.status_code} for postcode {postcode}')
            return None
        except requests.RequestException as exc:
            print(f'  ✗ Request error (attempt {attempt}): {exc}')
            time.sleep(wait)
            wait = min(wait * 2, 160)
    return None


# ── Response parser ───────────────────────────────────────────────────────────

def _parse_restaurant(r):
    """
    Parse a single restaurant object from the Just Eat enriched API response.

    The API returns structures like:
      {
        "name": "...",
        "uniqueName": "restaurant-name-bs1",
        "address": {
          "firstLine": "123 High Street",
          "city": "Bristol",
          "postCode": "BS1 6AQ"
        },
        "cuisines": [{"name": "...", "uniqueName": "..."}, ...]
      }

    URL pattern: https://www.just-eat.co.uk/restaurants-{uniqueName}/menu
    """
    try:
        name = r.get('name', '').strip()
        unique_name = r.get('uniqueName', '').strip()

        if not name or not unique_name:
            return None

        addr_obj = r.get('address', {})
        if isinstance(addr_obj, dict):
            parts = [
                addr_obj.get('firstLine', ''),
                addr_obj.get('city', ''),
                addr_obj.get('postCode', ''),
            ]
            address = ', '.join(p for p in parts if p)
            postcode = _normalise_postcode(addr_obj.get('postCode', ''))
        else:
            address = str(addr_obj)
            postcode = _extract_postcode(address)

        cuisines_raw = r.get('cuisines', [])
        if isinstance(cuisines_raw, list):
            cuisines = ' • '.join(
                c.get('name', '') for c in cuisines_raw
                if isinstance(c, dict) and c.get('name')
            )
        else:
            cuisines = ''

        url = f'https://www.just-eat.co.uk/restaurants-{unique_name}/menu'

        return {
            'service': 'justeat',
            'name': name,
            'address': address.strip(),
            'postcode': postcode,
            'url': url,
            'cuisines': cuisines,
            '_unique_name': unique_name,  # used for dedup, stripped before saving
        }
    except (AttributeError, KeyError, TypeError):
        return None


# ── Checkpoint save ───────────────────────────────────────────────────────────

def _save(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in FIELDNAMES})


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='Just Eat UK restaurant scraper')
    parser.add_argument('--postcode', action='append', dest='postcodes', metavar='PC',
                        help='Specific postcode(s) to query (repeatable). '
                             'Defaults to postcodes extracted from listings.csv.')
    parser.add_argument('--limit', type=int, default=None,
                        help='Process at most this many postcodes (for testing)')
    args = parser.parse_args()

    print('=' * 60)
    print('JUST EAT UK RESTAURANT SCRAPER')
    print('=' * 60)

    # ── Load existing output ──────────────────────────────────────────────────
    existing_unique_names = set()
    existing_rows = []
    if os.path.exists(OUTPUT_CSV):
        print(f'\n[INIT] Loading existing CSV: {OUTPUT_CSV}')
        with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_rows.append(row)
                # Derive unique_name from URL
                url = row.get('url', '')
                m = re.search(r'/restaurants-([^/]+)/menu', url)
                if m:
                    existing_unique_names.add(m.group(1))
        print(f'  ✓ {len(existing_unique_names)} existing restaurants loaded')

    # ── Determine postcodes ───────────────────────────────────────────────────
    if args.postcodes:
        postcodes = [_normalise_postcode(p) for p in args.postcodes]
        print(f'\n[INIT] Using {len(postcodes)} provided postcode(s)')
    else:
        print(f'\n[INIT] Reading postcodes from: {LISTINGS_CSV}')
        postcodes = _read_postcodes_from_listings(LISTINGS_CSV)
        print(f'  Found {len(postcodes)} unique postcodes')

    if args.limit:
        postcodes = postcodes[:args.limit]
        print(f'  Capped to {len(postcodes)} postcodes')

    if not postcodes:
        print('✗ No postcodes to process. Aborting.')
        return

    # ── Query API per postcode ────────────────────────────────────────────────
    print(f'\n[STEP] Querying Just Eat API for {len(postcodes)} postcodes…')
    rows = existing_rows.copy()
    seen_unique_names = set(existing_unique_names)
    new_count = 0
    failed = 0

    session = requests.Session()

    for i, postcode in enumerate(postcodes, 1):
        print(f'[{i}/{len(postcodes)}] {postcode}', end=' ')
        time.sleep(REQUEST_DELAY)

        data = _get_json(session, postcode)
        if data is None:
            failed += 1
            print('✗ API error')
            continue

        restaurants = data.get('restaurants', [])
        added = 0
        for r in restaurants:
            parsed = _parse_restaurant(r)
            if parsed is None:
                continue
            unique_name = parsed.pop('_unique_name')
            if unique_name in seen_unique_names:
                continue
            seen_unique_names.add(unique_name)
            rows.append(parsed)
            added += 1
            new_count += 1

        print(f'→ {len(restaurants)} returned, {added} new')

        if i % CHECKPOINT_EVERY == 0:
            print(f'  💾 Checkpoint at postcode {i}…')
            _save(rows, OUTPUT_CSV)
            print(f'  ✓ Saved {len(rows)} total rows')

    # ── Final save ────────────────────────────────────────────────────────────
    _save(rows, OUTPUT_CSV)
    print(f'\n{"=" * 60}')
    print(f'✓ Done. {new_count} new restaurants found.')
    print(f'✓ Total rows in {OUTPUT_CSV}: {len(rows)}')
    print('=' * 60)


if __name__ == '__main__':
    main()
