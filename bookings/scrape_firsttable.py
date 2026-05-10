"""
First Table UK restaurant scraper — city listing pages.

Strategy:
  First Table lists restaurants by city at:
    https://www.firsttable.co.uk/{city-slug}

  Restaurants load client-side (Next.js), so Playwright is required.

  Steps:
  1. Read unique city slugs from bookings/listings.csv
  2. For each city, open the city page in a headless browser
  3. Scroll to load all lazy-loaded restaurant cards
  4. Extract restaurant links with 3-segment paths: /{city}/{suburb}/{slug}
  5. Save incrementally to bookings/firsttable.csv

Output CSV columns:
  service, name, city, address, url

Usage:
  python bookings/scrape_firsttable.py
  python bookings/scrape_firsttable.py --city bristol --city london
  python bookings/scrape_firsttable.py --limit 5
  python bookings/scrape_firsttable.py --headed
"""

import os
import csv
import time
import re
import argparse
from urllib.parse import urljoin

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

# ── Constants ────────────────────────────────────────────────────────────────

LISTINGS_CSV = 'bookings/listings.csv'
OUTPUT_CSV = 'bookings/firsttable.csv'
CHECKPOINT_EVERY = 5
PAGE_LOAD_TIMEOUT = 30_000   # ms
SCROLL_PAUSE = 2.5           # seconds between scrolls
MAX_SCROLL_ATTEMPTS = 20     # max scrolls to load lazy content

BASE_DOMAIN = 'https://www.firsttable.co.uk'

# City slug mapping: our listing city_slug → First Table URL slug.
# Verify/extend by checking https://www.firsttable.co.uk
CITY_SLUGS = {
    'bristol':      'bristol',
    'london':       'london',
    'manchester':   'manchester',
    'birmingham':   'birmingham',
    'edinburgh':    'edinburgh',
    'glasgow':      'glasgow',
    'leeds':        'leeds',
    'liverpool':    'liverpool',
    'cardiff':      'cardiff',
    'bath':         'bath',
    'oxford':       'oxford',
    'cambridge':    'cambridge',
    'brighton':     'brighton',
    'sheffield':    'sheffield',
    'nottingham':   'nottingham',
    'newcastle':    'newcastle-upon-tyne',
    'exeter':       'exeter',
    'york':         'york',
    'chester':      'chester',
    'coventry':     'coventry',
}

FIELDNAMES = ['service', 'name', 'city', 'address', 'url']


# ── Playwright page scraper ────────────────────────────────────────────────────

def _load_and_scroll(pw_page, url, ft_slug, label):
    """
    Navigate to *url*, dismiss cookie banner, then scroll until all lazy
    restaurant cards have loaded.  Returns the card selector used.
    Raises PWTimeoutError / returns None on failure.
    """
    print(f'  Loading: {url}')
    try:
        pw_page.goto(url, timeout=PAGE_LOAD_TIMEOUT, wait_until='domcontentloaded')
    except PWTimeoutError:
        print(f'  ✗ Timeout loading "{label}"')
        return None

    # Dismiss cookie banner if present
    for selector in ['button:has-text("Accept")', 'button:has-text("OK")',
                     '[class*="cookie"] button', '[id*="cookie"] button']:
        try:
            btn = pw_page.locator(selector).first
            if btn.is_visible(timeout=2000):
                btn.click(timeout=2000)
                break
        except PWTimeoutError:
            pass

    card_sel = f'a[href*="/{ft_slug}/"]'
    try:
        pw_page.wait_for_selector(card_sel, timeout=15_000)
    except PWTimeoutError:
        print(f'  ✗ No restaurant cards appeared for "{label}" — '
              f'check CITY_SLUGS mapping.')
        return None

    # Scroll to trigger lazy-loading
    prev_count = 0
    stale_scrolls = 0
    for scroll_n in range(MAX_SCROLL_ATTEMPTS):
        pw_page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        time.sleep(SCROLL_PAUSE)
        count = pw_page.locator(card_sel).count()
        if count == prev_count:
            stale_scrolls += 1
            if stale_scrolls >= 3:
                break
        else:
            stale_scrolls = 0
            prev_count = count
        print(f'    scroll {scroll_n + 1}: {count} links visible', end='\r')
    print()
    return card_sel


def _extract_restaurants(pw_page, ft_slug, city_slug, existing_urls):
    """
    Extract 3-segment restaurant links from the current page.
    Also returns 2-segment suburb page URLs discovered on the same page.
    Returns (results_list, suburb_urls_set).
    """
    card_sel = f'a[href*="/{ft_slug}/"]'
    heading_sel = (
        f'h2 a[href*="/{ft_slug}/"], '
        f'h3 a[href*="/{ft_slug}/"], '
        f'h4 a[href*="/{ft_slug}/"]'
    )

    results_map = {}   # url → row dict
    suburb_urls = set()

    def _process_anchor(anchor, is_heading):
        try:
            href = anchor.get_attribute('href') or ''
        except Exception:
            return
        href = href.split('#')[0]
        full_url = urljoin(BASE_DOMAIN, href) if not href.startswith('http') else href
        full_url = full_url.rstrip('/')
        path_parts = [p for p in full_url.replace(BASE_DOMAIN, '').split('/') if p]

        if len(path_parts) == 2:
            # Suburb listing page — collect for follow-up scraping
            suburb_urls.add(full_url)
            return

        if len(path_parts) != 3:
            return
        if full_url in existing_urls and not is_heading:
            return

        name = ''
        try:
            name = (anchor.inner_text() or '').strip()
        except Exception:
            pass
        name = re.sub(r'\s*[›»].*$', '', name).strip()
        name = re.sub(r'^(Top Rated #\d+|New Addition|Featured)\s*', '', name).strip()

        suburb = path_parts[1].replace('-', ' ').title() if len(path_parts) >= 2 else ''
        row = {
            'service': 'firsttable',
            'name': name,
            'city': city_slug,
            'address': suburb,
            'url': full_url,
        }
        if full_url not in results_map or (is_heading and name):
            results_map[full_url] = row

    for anchor in pw_page.locator(heading_sel).all():
        _process_anchor(anchor, is_heading=True)
    for anchor in pw_page.locator(card_sel).all():
        _process_anchor(anchor, is_heading=False)

    results = []
    for full_url, row in results_map.items():
        if full_url not in existing_urls:
            results.append(row)
            existing_urls.add(full_url)

    return results, suburb_urls


def _scrape_city(pw_page, city_slug, existing_urls, headed=False):
    """
    Scrape the city listing page, then follow every suburb page discovered
    on it to ensure complete coverage of all restaurants.
    """
    ft_slug = CITY_SLUGS.get(city_slug, city_slug)
    city_url = f'{BASE_DOMAIN}/{ft_slug}'
    all_results = []

    # ── City-level page ────────────────────────────────────────────────────
    card_sel = _load_and_scroll(pw_page, city_url, ft_slug, city_slug)
    if card_sel is None:
        return all_results

    city_results, suburb_urls = _extract_restaurants(
        pw_page, ft_slug, city_slug, existing_urls)
    all_results.extend(city_results)
    print(f'  City page: {len(city_results)} new restaurants, '
          f'{len(suburb_urls)} suburbs found')

    # ── Suburb pages ───────────────────────────────────────────────────────
    for suburb_url in sorted(suburb_urls):
        suburb_label = suburb_url.replace(BASE_DOMAIN, '').strip('/')
        sub_card_sel = _load_and_scroll(pw_page, suburb_url, ft_slug, suburb_label)
        if sub_card_sel is None:
            continue
        sub_results, _ = _extract_restaurants(
            pw_page, ft_slug, city_slug, existing_urls)
        all_results.extend(sub_results)
        print(f'    {suburb_label}: {len(sub_results)} new')

    return all_results


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
    parser = argparse.ArgumentParser(description='First Table UK restaurant scraper')
    parser.add_argument('--city', action='append', dest='cities', metavar='SLUG',
                        help='City slug(s) to scrape (repeatable). '
                             'Defaults to cities from listings.csv.')
    parser.add_argument('--limit', type=int, default=None,
                        help='Process at most this many cities')
    parser.add_argument('--headed', action='store_true',
                        help='Run browser in headed (visible) mode')
    args = parser.parse_args()

    print('=' * 60)
    print('FIRST TABLE UK RESTAURANT SCRAPER')
    print('=' * 60)

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

    if args.cities:
        cities = [c.lower().strip() for c in args.cities]
    else:
        cities = _read_city_slugs(LISTINGS_CSV)
        print(f'\n[INIT] Found {len(cities)} cities in listings: {cities}')

    if args.limit:
        cities = cities[:args.limit]

    if not cities:
        print('✗ No cities to process. Aborting.')
        return

    print(f'\n[STEP] Scraping {len(cities)} cities…')
    rows = existing_rows.copy()
    total_new = 0

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=not args.headed)
        context = browser.new_context(
            user_agent=(
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
            ),
            locale='en-GB',
        )
        pw_page = context.new_page()

        for i, city_slug in enumerate(cities, 1):
            print(f'\n[{i}/{len(cities)}] {city_slug}')
            new_results = _scrape_city(pw_page, city_slug, existing_urls,
                                       headed=args.headed)
            rows.extend(new_results)
            total_new += len(new_results)
            print(f'  → {len(new_results)} new for {city_slug}')

            if i % CHECKPOINT_EVERY == 0:
                print(f'  💾 Checkpoint at city {i}…')
                _save(rows, OUTPUT_CSV)
                print(f'  ✓ Saved {len(rows)} total rows')

        browser.close()

    _save(rows, OUTPUT_CSV)
    print(f'\n{"=" * 60}')
    print(f'✓ Done. {total_new} new restaurants found.')
    print(f'✓ Total rows in {OUTPUT_CSV}: {len(rows)}')
    print('=' * 60)


if __name__ == '__main__':
    main()
