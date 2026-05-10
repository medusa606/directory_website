"""
DesignMyNight UK restaurant/venue scraper — Playwright approach.

Strategy:
  DesignMyNight is a heavily JavaScript-rendered site. Venue listings per city
  are split across category pages:
    https://www.designmynight.com/{city-slug}/restaurants
    https://www.designmynight.com/{city-slug}/bars
    https://www.designmynight.com/{city-slug}/pubs
    https://www.designmynight.com/{city-slug}/clubs

  Venue URLs follow the pattern: /{city}/{category}/{neighbourhood}/{slug}
  (4-segment path). Editorial/list pages use 3-segment paths and are excluded.

  Steps:
  1. Read unique city slugs from bookings/listings.csv
  2. For each city + category, load the listing page with Playwright
  3. Scroll/paginate to load all results (infinite scroll or paginator)
  4. Extract: name, URL, address per venue card
  5. Save incrementally to bookings/designmynight.csv

  Note: DesignMyNight covers UK cities well but has strongest data for London.

Output CSV columns:
  service, name, city, address, url

Usage:
  python bookings/scrape_designmynight.py
  python bookings/scrape_designmynight.py --city bristol --city london
  python bookings/scrape_designmynight.py --limit 3
  python bookings/scrape_designmynight.py --headed
"""

import os
import csv
import time
import re
import argparse

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout

# ── Constants ────────────────────────────────────────────────────────────────

LISTINGS_CSV = 'bookings/listings.csv'
OUTPUT_CSV = 'bookings/designmynight.csv'
CHECKPOINT_EVERY = 3

# Category listing pages — venue URLs within these pages are scraped
VENUE_CATEGORIES = ['restaurants', 'bars', 'pubs', 'clubs']
BASE_URL = 'https://www.designmynight.com/{city}/{category}'
BASE_DOMAIN = 'https://www.designmynight.com'

# Venue URLs require at least 2 path segments after the category
# (city/category/neighbourhood/slug) to avoid matching editorial list pages
# which only have city/category/editorial-slug (3 parts total)
VENUE_URL_RE = re.compile(
    r'designmynight\.com/[^/]+/(restaurants|bars|pubs|clubs|nightclubs)/[^/]+/[^/?#]+'
)

PAGE_LOAD_WAIT_MS = 4000
SCROLL_WAIT_MS = 2000
INTER_CITY_DELAY = 3.0
MAX_SCROLL_ATTEMPTS = 15    # limit infinite scroll loops

# DesignMyNight city slug mapping: our city_slug → DMN city slug
# Verify by visiting designmynight.com and checking the URL
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
    'newcastle':    'newcastle',
    'exeter':       'exeter',
    'york':         'york',
    'chester':      'chester',
    'coventry':     'coventry',
}

FIELDNAMES = ['service', 'name', 'city', 'address', 'url']


# ── Playwright scraping ───────────────────────────────────────────────────────

def _dismiss_overlays(page):
    """Dismiss cookie banners and modals if present."""
    for selector in [
        'button[aria-label*="cookie" i]',
        'button[id*="accept" i]',
        'button:has-text("Accept all")',
        'button:has-text("Accept")',
        'button:has-text("OK")',
        '[class*="cookie"] button',
        '[id*="cookie"] button',
    ]:
        try:
            btn = page.locator(selector).first
            if btn.is_visible(timeout=1500):
                btn.click(timeout=1500)
                page.wait_for_timeout(500)
                break
        except PlaywrightTimeout:
            pass


def _extract_cards(page, city_slug):
    """
    Extract all visible venue cards from the page.
    Returns list of {'name': ..., 'city': ..., 'address': ..., 'url': ...}.
    """
    results = []
    seen_urls = set()

    # DMN venue links: /{city}/{category}/{neighbourhood}/{slug}
    # Match links containing any of the venue category path segments
    anchors = page.locator(
        'a[href*="/restaurants/"], a[href*="/bars/"], '
        'a[href*="/pubs/"], a[href*="/clubs/"]'
    ).all()

    for anchor in anchors:
        try:
            href = anchor.get_attribute('href') or ''
            if not href:
                continue
            full_url_candidate = href if href.startswith('http') else BASE_DOMAIN + href
            # Only process 4-segment venue URLs; skip editorial/list pages
            if not VENUE_URL_RE.search(full_url_candidate):
                continue
            if full_url_candidate in seen_urls:
                continue
            seen_urls.add(full_url_candidate)

            full_url = href if href.startswith('http') else BASE_DOMAIN + href

            # Name: aria-label or heading text
            name = anchor.get_attribute('aria-label') or ''
            if not name:
                # Try heading inside the link
                heading = anchor.locator('h2, h3, h4').first
                try:
                    name = heading.inner_text(timeout=1000).strip()
                except PlaywrightTimeout:
                    pass
            if not name:
                try:
                    raw = anchor.inner_text(timeout=1000).strip()
                    name = raw.splitlines()[0].strip()[:80]
                except PlaywrightTimeout:
                    pass

            # Address: look in card container for address-like text
            address = ''
            try:
                card = anchor.locator('xpath=ancestor::article | xpath=ancestor::li | xpath=ancestor::div[contains(@class,"card")] | xpath=ancestor::div[contains(@class,"venue")]').first
                addr_candidates = card.locator('address, [itemprop="address"], [class*="address"], [class*="location"]').all()
                for el in addr_candidates:
                    text = el.inner_text(timeout=500).strip()
                    if text and len(text) > 3:
                        address = text
                        break
            except (PlaywrightTimeout, Exception):
                pass

            if name:
                results.append({
                    'service': 'designmynight',
                    'name': name,
                    'city': city_slug,
                    'address': address,
                    'url': full_url,
                })
        except PlaywrightTimeout:
            continue

    return results


def _scrape_city(page, city_slug, existing_urls):
    """
    Scrape all venues for a city across all categories using infinite scroll.
    Returns list of new result dicts.
    """
    dmn_slug = CITY_SLUGS.get(city_slug, city_slug)
    results = []

    for category in VENUE_CATEGORIES:
        start_url = BASE_URL.format(city=dmn_slug, category=category)
        results.extend(_scrape_city_category(page, city_slug, category, start_url, existing_urls))
        time.sleep(1.5)

    return results


def _scrape_city_category(page, city_slug, category, start_url, existing_urls):
    """
    Scrape one category listing page for a city.
    Returns list of new result dicts.
    """
    results = []

    try:
        print(f'  Loading: {start_url}')
        page.goto(start_url, wait_until='domcontentloaded', timeout=25000)
        page.wait_for_timeout(PAGE_LOAD_WAIT_MS)
        _dismiss_overlays(page)

        prev_count = 0
        scroll_attempt = 0

        while scroll_attempt < MAX_SCROLL_ATTEMPTS:
            cards = _extract_cards(page, city_slug)
            current_count = len(cards)

            new_on_scroll = 0
            for card in cards:
                if card['url'] not in existing_urls:
                    results.append(card)
                    existing_urls.add(card['url'])
                    new_on_scroll += 1

            print(f'  Scroll {scroll_attempt + 1}: {current_count} cards visible, '
                  f'{new_on_scroll} new this pass')

            # Check for "Load more" button
            loaded_more = False
            for selector in [
                'button:has-text("Load more")',
                'button:has-text("Show more")',
                'a:has-text("Load more")',
                'button[class*="load-more"]',
                'button[class*="loadmore"]',
            ]:
                try:
                    btn = page.locator(selector).first
                    if btn.is_visible(timeout=1500):
                        btn.click(timeout=2000)
                        page.wait_for_timeout(SCROLL_WAIT_MS)
                        loaded_more = True
                        break
                except PlaywrightTimeout:
                    pass

            if not loaded_more:
                # Scroll to bottom to trigger infinite scroll
                page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
                page.wait_for_timeout(SCROLL_WAIT_MS)

            # Check for next-page link
            try:
                next_link = page.locator('a[rel="next"]').first
                if next_link.is_visible(timeout=1000):
                    next_href = next_link.get_attribute('href') or ''
                    if next_href:
                        page.goto(next_href if next_href.startswith('http')
                                  else BASE_DOMAIN + next_href,
                                  wait_until='domcontentloaded', timeout=20000)
                        page.wait_for_timeout(PAGE_LOAD_WAIT_MS)
                        scroll_attempt += 1
                        prev_count = 0
                        continue
            except PlaywrightTimeout:
                pass

            # Stop if card count stopped growing
            if current_count <= prev_count:
                break
            prev_count = current_count
            scroll_attempt += 1

    except PlaywrightTimeout:
        print(f'  ⚠ Page load timeout for "{city_slug}/{category}"')
    except Exception as exc:
        print(f'  ✗ Error scraping "{city_slug}/{category}": {exc}')

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
    parser = argparse.ArgumentParser(description='DesignMyNight UK venue scraper')
    parser.add_argument('--city', action='append', dest='cities', metavar='SLUG',
                        help='City slug(s) to scrape (repeatable). '
                             'Defaults to cities from listings.csv.')
    parser.add_argument('--limit', type=int, default=None,
                        help='Process at most this many cities')
    parser.add_argument('--headed', action='store_true',
                        help='Run browser in headed mode for debugging')
    args = parser.parse_args()

    print('=' * 60)
    print('DESIGNMYNIGHT UK VENUE SCRAPER')
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
        print(f'  ✓ {len(existing_urls)} existing venues loaded')

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

    print(f'\n[STEP] Scraping {len(cities)} cities via Playwright…')
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
        page = context.new_page()

        for i, city_slug in enumerate(cities, 1):
            print(f'\n[{i}/{len(cities)}] {city_slug}')
            time.sleep(INTER_CITY_DELAY)

            new_results = _scrape_city(page, city_slug, existing_urls)
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
    print(f'✓ Done. {total_new} new venues found.')
    print(f'✓ Total rows in {OUTPUT_CSV}: {len(rows)}')
    print('=' * 60)


if __name__ == '__main__':
    main()
