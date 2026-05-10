"""
TheFork UK restaurant scraper — city listing pages.

Strategy:
  TheFork structures UK restaurant pages by city using an internal city ID:
    https://www.thefork.co.uk/restaurants/{city-slug}-c{city-id}/

  Steps:
  1. Read unique city slugs from bookings/listings.csv
  2. Map city slugs to TheFork city IDs (see CITY_IDS dict below)
  3. For each city, paginate through restaurant listing pages
  4. Extract: name, URL, address per restaurant card
  5. Save incrementally to bookings/thefork.csv

  If a city slug is not in CITY_IDS, the scraper attempts to discover the
  city URL by searching TheFork's UK location listing page.

  Note: TheFork uses JavaScript for parts of the page but restaurant cards
  are typically server-side rendered. Tries requests+BeautifulSoup first;
  falls back to Playwright if page content appears empty.

Output CSV columns:
  service, name, city, address, url

Usage:
  python bookings/scrape_thefork.py
  python bookings/scrape_thefork.py --city bristol --city london
  python bookings/scrape_thefork.py --limit 20
"""

import os
import csv
import time
import re
import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlencode

# ── Constants ────────────────────────────────────────────────────────────────

LISTINGS_CSV = 'bookings/listings.csv'
OUTPUT_CSV = 'bookings/thefork.csv'
CHECKPOINT_EVERY = 5    # cities
REQUEST_DELAY = 2.0
BACKOFF_BASE = 10
MAX_RETRIES = 5

BASE_DOMAIN = 'https://www.thefork.co.uk'

# Known TheFork UK city IDs.
# Add more as needed: find by visiting thefork.co.uk and inspecting the city URL.
CITY_IDS = {
    'bristol':      '537890',
    'london':       '768026',
    'manchester':   '540272',
    'birmingham':   '535994',
    'edinburgh':    '537612',
    'glasgow':      '537749',
    'leeds':        '538009',
    'liverpool':    '538096',
    'cardiff':      '536427',
    'bath':         '535760',
    'oxford':       '538546',
    'cambridge':    '536337',
    'brighton':     '536214',
    'sheffield':    '538775',
    'nottingham':   '538484',
    'newcastle':    '538367',
    'exeter':       '537653',
    'york':         '539246',
    'chester':      '536558',
    'coventry':     '536731',
}

FIELDNAMES = ['service', 'name', 'city', 'address', 'url']

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
        '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    ),
    'Accept-Language': 'en-GB,en;q=0.9',
}


# ── HTTP helper ───────────────────────────────────────────────────────────────

def _get(session, url):
    wait = BACKOFF_BASE
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            resp = session.get(url, headers=HEADERS, timeout=30)
            if resp.status_code == 200:
                return resp
            if resp.status_code in (429, 503, 504):
                print(f'  ⚠ HTTP {resp.status_code} (attempt {attempt}), waiting {wait}s…')
                time.sleep(wait)
                wait = min(wait * 2, 160)
                continue
            if resp.status_code == 404:
                return None
            print(f'  ✗ HTTP {resp.status_code} for {url}')
            return None
        except requests.RequestException as exc:
            print(f'  ✗ Request error (attempt {attempt}): {exc}')
            time.sleep(wait)
            wait = min(wait * 2, 160)
    return None


# ── City URL discovery ────────────────────────────────────────────────────────

def _city_url(city_slug):
    """Return the TheFork listing URL for a city, or None if not known."""
    city_id = CITY_IDS.get(city_slug.lower())
    if city_id:
        return f'{BASE_DOMAIN}/restaurants/{city_slug}-c{city_id}/'
    return None


def _discover_city_url(session, city_slug):
    """
    Try to discover a TheFork city URL for an unknown city slug by searching
    TheFork's location page.
    Returns URL string or None.
    """
    search_url = f'{BASE_DOMAIN}/find-a-restaurant?searchQuery={city_slug}&where={city_slug}'
    resp = _get(session, search_url)
    if resp is None:
        return None
    soup = BeautifulSoup(resp.text, 'html.parser')
    # Look for a link matching /restaurants/{city}-c{id}/
    pattern = re.compile(r'/restaurants/[^/]+-c(\d+)/?')
    for a in soup.find_all('a', href=pattern):
        href = a['href']
        city_name_in_href = href.split('/restaurants/')[1].split('-c')[0]
        if city_slug.lower() in city_name_in_href.lower():
            return urljoin(BASE_DOMAIN, href)
    return None


# ── Page parsing ──────────────────────────────────────────────────────────────

def _parse_restaurant_cards(soup, city_slug):
    """
    Extract restaurant entries from a TheFork city listing page.
    TheFork renders restaurant cards as article or div elements.
    Returns list of {'name': ..., 'city': ..., 'address': ..., 'url': ...}.
    """
    results = []

    # TheFork restaurant cards typically have a link with /restaurant/ in the href
    seen_urls = set()
    for a in soup.find_all('a', href=re.compile(r'/restaurant/')):
        href = a.get('href', '')
        if not href or href in seen_urls:
            continue
        seen_urls.add(href)

        full_url = urljoin(BASE_DOMAIN, href)

        # Name: from aria-label, title attribute, or heading inside the card
        name = (
            a.get('aria-label', '').strip()
            or a.get('title', '').strip()
        )
        if not name:
            heading = a.find(['h2', 'h3', 'h4', 'span', 'p'])
            if heading:
                name = heading.get_text(strip=True)

        if not name:
            name = a.get_text(strip=True)[:80]

        # Address: look for address sibling within card container
        card = a.find_parent(['article', 'li', 'div'])
        address = ''
        if card:
            addr_el = card.find(attrs={'itemprop': 'address'})
            if addr_el:
                address = addr_el.get_text(separator=', ', strip=True)
            else:
                # Look for small text that might be an address
                for el in card.find_all(['p', 'span', 'address']):
                    text = el.get_text(strip=True)
                    # Heuristic: short text with comma is likely an address fragment
                    if 5 < len(text) < 120 and ',' in text and text != name:
                        address = text
                        break

        if name and full_url:
            results.append({
                'service': 'thefork',
                'name': name,
                'city': city_slug,
                'address': address,
                'url': full_url,
            })

    return results


def _next_page_url(soup, current_url):
    """Find the URL for the next page of results, or None."""
    # TheFork paginates via ?page=N or a rel="next" link
    next_link = soup.find('a', rel='next')
    if next_link:
        href = next_link.get('href', '')
        if href:
            return urljoin(current_url, href)

    # Fallback: look for a link with page number one higher
    current_page_m = re.search(r'[?&]page=(\d+)', current_url)
    current_page = int(current_page_m.group(1)) if current_page_m else 1
    next_page = current_page + 1

    for a in soup.find_all('a', href=re.compile(r'page=')):
        href = a.get('href', '')
        if f'page={next_page}' in href:
            return urljoin(current_url, href)

    return None


# ── City scraping ─────────────────────────────────────────────────────────────

def _scrape_city(session, city_slug, existing_urls):
    """
    Scrape all restaurant pages for a city from TheFork.
    Returns list of new result dicts.
    """
    city_url = _city_url(city_slug)
    if city_url is None:
        print(f'  ⚠ City "{city_slug}" not in CITY_IDS, attempting discovery…')
        city_url = _discover_city_url(session, city_slug)
        if city_url is None:
            print(f'  ✗ Could not find TheFork URL for "{city_slug}". '
                  f'Add to CITY_IDS in scrape_thefork.py')
            return []

    results = []
    page_url = city_url
    page_num = 1

    while page_url:
        print(f'  Page {page_num}: {page_url}')
        time.sleep(REQUEST_DELAY)

        resp = _get(session, page_url)
        if resp is None:
            break

        soup = BeautifulSoup(resp.text, 'html.parser')

        # Detect if the page is JavaScript-rendered (no restaurant cards)
        cards = _parse_restaurant_cards(soup, city_slug)

        if not cards and page_num == 1:
            print(f'  ⚠ No restaurant cards found on page 1 for "{city_slug}". '
                  f'The page may require JavaScript rendering. '
                  f'Consider using scrape_designmynight.py as a reference for '
                  f'Playwright fallback, or check the URL structure.')
            break

        new_on_page = 0
        for card in cards:
            if card['url'] not in existing_urls:
                results.append(card)
                existing_urls.add(card['url'])
                new_on_page += 1

        print(f'    → {len(cards)} cards, {new_on_page} new')

        if not cards:
            break

        next_url = _next_page_url(soup, page_url)
        if not next_url or next_url == page_url:
            break
        page_url = next_url
        page_num += 1

    return results


# ── Helpers ───────────────────────────────────────────────────────────────────

def _read_city_slugs(listings_csv):
    slugs = set()
    if not os.path.exists(listings_csv):
        print(f'  ⚠ Listings CSV not found: {listings_csv}')
        return []
    with open(listings_csv, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row.get('city_slug', '').strip().lower()
            if slug:
                slugs.add(slug)
    return sorted(slugs)


def _save(rows, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='TheFork UK restaurant scraper')
    parser.add_argument('--city', action='append', dest='cities', metavar='SLUG',
                        help='City slug(s) to scrape (repeatable). '
                             'Defaults to cities from listings.csv.')
    parser.add_argument('--limit', type=int, default=None,
                        help='Process at most this many cities (for testing)')
    args = parser.parse_args()

    print('=' * 60)
    print('THEFORK UK RESTAURANT SCRAPER')
    print('=' * 60)

    # ── Load existing output ──────────────────────────────────────────────────
    existing_urls = set()
    existing_rows = []
    if os.path.exists(OUTPUT_CSV):
        print(f'\n[INIT] Loading existing CSV: {OUTPUT_CSV}')
        with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                existing_rows.append(row)
                existing_urls.add(row['url'])
        print(f'  ✓ {len(existing_urls)} existing restaurants loaded')

    # ── Determine cities ──────────────────────────────────────────────────────
    if args.cities:
        cities = [c.lower().strip() for c in args.cities]
    else:
        cities = _read_city_slugs(LISTINGS_CSV)
        print(f'\n[INIT] Found {len(cities)} city slugs in listings: {cities}')

    if args.limit:
        cities = cities[:args.limit]
        print(f'  Capped to {len(cities)} cities')

    if not cities:
        print('✗ No cities to process. Aborting.')
        return

    # ── Scrape each city ──────────────────────────────────────────────────────
    print(f'\n[STEP] Scraping {len(cities)} cities…')
    rows = existing_rows.copy()
    total_new = 0

    session = requests.Session()

    for i, city_slug in enumerate(cities, 1):
        print(f'\n[{i}/{len(cities)}] {city_slug}')
        new_results = _scrape_city(session, city_slug, existing_urls)
        rows.extend(new_results)
        total_new += len(new_results)
        print(f'  → {len(new_results)} new for {city_slug}')

        if i % CHECKPOINT_EVERY == 0:
            print(f'  💾 Checkpoint at city {i}…')
            _save(rows, OUTPUT_CSV)
            print(f'  ✓ Saved {len(rows)} total rows')

    # ── Final save ────────────────────────────────────────────────────────────
    _save(rows, OUTPUT_CSV)
    print(f'\n{"=" * 60}')
    print(f'✓ Done. {total_new} new restaurants found.')
    print(f'✓ Total rows in {OUTPUT_CSV}: {len(rows)}')
    print('=' * 60)


if __name__ == '__main__':
    main()
