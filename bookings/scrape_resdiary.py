"""
ResDiary UK restaurant scraper — DuckDuckGo search approach.

Strategy:
  ResDiary has migrated to DishCult (dishcult.com). Restaurant booking
  pages are indexed by search engines. We search for each listing by name
  and city, targeting dishcult.com results.

  Search query pattern:
    site:dishcult.com "{name}" {city}
  or fallback:
    site:dishcult.com {name} {city} restaurant

  Steps:
  1. Read listings from bookings/listings.csv (id, name, city_slug, address)
  2. For each listing, run a ddgs search for the above query
  3. If a dishcult.com URL is found and name confidence is sufficient, record it
  4. Save incrementally to bookings/resdiary.csv

  Rate limit: ddgs enforces rate limits; uses 2s delay + 30s backoff on 429.
  Checkpoint save every CHECKPOINT_EVERY listings.

  Note: This script searches per-listing so it's inherently slow for large
  datasets. Run with --limit for testing, or --status new to skip already
  searched listings.

Output CSV columns:
  service, name, city, url
  (name/city come from the search result, not the listing — for match_booking_urls.py
   to re-verify via fuzzy matching)

Also writes bookings/resdiary_search_log.csv with columns:
  listing_id, listing_name, listing_city, query, found_url, skipped_reason

Usage:
  python bookings/scrape_resdiary.py
  python bookings/scrape_resdiary.py --limit 50
  python bookings/scrape_resdiary.py --listing-id <uuid>
"""

import os
import csv
import time
import re
import argparse
import signal
import multiprocessing

try:
    from ddgs import DDGS
except ImportError:
    print("ERROR: ddgs package not installed. Run: pip install ddgs")
    raise

# ── Constants ────────────────────────────────────────────────────────────────

LISTINGS_CSV = 'bookings/listings.csv'
OUTPUT_CSV = 'bookings/resdiary.csv'
LOG_CSV = 'bookings/resdiary_search_log.csv'

CHECKPOINT_EVERY = 10
SEARCH_DELAY = 2.5          # seconds between searches
RATELIMIT_BACKOFF = 35      # seconds to wait after rate limit hit

MAX_RESULTS_PER_QUERY = 5
WORKERS = 10
DDGS_TIMEOUT = 12           # seconds before a single ddgs request times out

FIELDNAMES = ['service', 'name', 'city', 'url']
LOG_FIELDNAMES = ['listing_id', 'listing_name', 'listing_city', 'query', 'found_url', 'skipped_reason']

DISHCULT_URL_RE = re.compile(
    r'https?://(?:www\.)?dishcult\.com/restaurant/([^/?#\s]+)',
    re.IGNORECASE
)


# ── ddgs search ───────────────────────────────────────────────────────────────

def _do_search(query):
    """Run a ddgs search with rate-limit retry. Returns list of result dicts."""
    try:
        return DDGS(timeout=DDGS_TIMEOUT).text(query, max_results=MAX_RESULTS_PER_QUERY)
    except Exception as e:
        error_msg = str(e).lower()
        if 'ratelimit' in error_msg:
            print(f'  ⚠ Rate limited, backing off {RATELIMIT_BACKOFF}s…')
            time.sleep(RATELIMIT_BACKOFF)
            try:
                return DDGS(timeout=DDGS_TIMEOUT).text(query, max_results=MAX_RESULTS_PER_QUERY)
            except Exception:
                print(f'  ✗ Rate limited again; skipping: {query}')
                return None
        else:
            print(f'  ✗ Search failed: {e}')
            return None


def _extract_resdiary_url(results):
    """
    Scan ddgs search results for a dishcult.com URL.
    Returns (url, result_title) or (None, None).
    """
    if not results:
        return None, None

    for result in results:
        href = result.get('href', '') or result.get('url', '')
        title = result.get('title', '')
        body = result.get('body', '')

        # Check URL directly
        m = DISHCULT_URL_RE.search(href)
        if m:
            return href, title

        # Check body text for embedded dishcult URLs
        m = DISHCULT_URL_RE.search(body)
        if m:
            return m.group(0), title

    return None, None


# ── Name confidence check ─────────────────────────────────────────────────────

def _name_words(name):
    """Return set of significant words from a name (lowercase, strip stopwords)."""
    stopwords = {'the', 'a', 'and', '&', 'of', 'at', 'in', 'on', 'for', 'restaurant', 'cafe', 'bar', 'bistro', 'kitchen', 'house'}
    words = re.findall(r'[a-z0-9]+', name.lower())
    return {w for w in words if w not in stopwords and len(w) > 2}


def _url_contains_name_words(url, listing_name, min_overlap=1):
    """
    Check that at least min_overlap significant words from listing_name
    appear in the URL slug. Avoids matching completely unrelated restaurants.
    """
    listing_words = _name_words(listing_name)
    if not listing_words:
        return True  # Can't check, allow through
    url_lower = url.lower()
    matches = sum(1 for w in listing_words if w in url_lower)
    return matches >= min_overlap


# ── Checkpoint saves ──────────────────────────────────────────────────────────

def _save(rows, path, fieldnames):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


# ── Per-listing search worker ─────────────────────────────────────────────────

def _worker_init():
    """Worker processes ignore SIGINT — main process handles Ctrl+C and terminates them."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def _search_listing(listing):
    """
    Worker: search ddgs for one listing.
    Returns (listing, candidate_url, used_query, skip_reason).
    Duplicate-URL check is deferred to the main thread (needs the shared lock).
    """
    name = listing['name']
    city_slug = listing['city_slug']
    city_display = city_slug.replace('-', ' ')

    query = f'site:dishcult.com "{name}" {city_display}'
    print(f'  Searching: {name} ({city_display})', flush=True)

    time.sleep(SEARCH_DELAY)
    results = _do_search(query)

    if results is None:
        return listing, None, query, 'search_error'

    candidate_url, _title = _extract_resdiary_url(results)

    if candidate_url is None:
        fallback_query = f'site:dishcult.com {name} {city_display} restaurant booking'
        print(f'  Fallback: {fallback_query}', flush=True)
        time.sleep(SEARCH_DELAY)
        fallback_results = _do_search(fallback_query)
        if fallback_results:
            candidate_url, _title = _extract_resdiary_url(fallback_results)
            if candidate_url:
                query = fallback_query

    if candidate_url and not _url_contains_name_words(candidate_url, name):
        print(f'  ⚠ URL name mismatch, skipping: {candidate_url}', flush=True)
        return listing, None, query, 'name_mismatch'

    return listing, candidate_url, query, ''


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='ResDiary search-based scraper')
    parser.add_argument('--limit', type=int, default=None,
                        help='Process at most this many listings (for testing)')
    parser.add_argument('--listing-id', dest='listing_id', default=None,
                        help='Process a single listing by ID')
    args = parser.parse_args()

    print('=' * 60)
    print('RESDIARY UK RESTAURANT SCRAPER (ddgs search)')
    print('=' * 60)

    # ── Load already-searched listing IDs from log ────────────────────────────
    already_searched = set()
    log_rows = []
    if os.path.exists(LOG_CSV):
        print(f'\n[INIT] Loading search log: {LOG_CSV}')
        with open(LOG_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                log_rows.append(row)
                already_searched.add(row['listing_id'])
        print(f'  ✓ {len(already_searched)} listings already searched')

    # ── Load existing output ──────────────────────────────────────────────────
    existing_urls = set()
    output_rows = []
    if os.path.exists(OUTPUT_CSV):
        print(f'\n[INIT] Loading existing CSV: {OUTPUT_CSV}')
        with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                output_rows.append(row)
                existing_urls.add(row['url'])
        print(f'  ✓ {len(output_rows)} existing ResDiary URLs loaded')

    # ── Load listings ─────────────────────────────────────────────────────────
    if not os.path.exists(LISTINGS_CSV):
        print(f'✗ Listings CSV not found: {LISTINGS_CSV}')
        return

    listings = []
    with open(LISTINGS_CSV, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            listing_id = row.get('id', '').strip()
            name = row.get('name', '').strip()
            city_slug = row.get('city_slug', '').strip()
            address = row.get('address', '').strip()
            if not name or not listing_id:
                continue
            if args.listing_id and listing_id != args.listing_id:
                continue
            if listing_id in already_searched:
                continue
            listings.append({
                'id': listing_id,
                'name': name,
                'city_slug': city_slug,
                'address': address,
            })

    if args.limit:
        listings = listings[:args.limit]

    print(f'\n[INIT] {len(listings)} listings to search (skipped {len(already_searched)} already done)')

    if not listings:
        print('✓ Nothing new to search.')
        return

    # ── Search per listing (parallel) ────────────────────────────────────────
    print(f'\n[STEP] Searching ddgs for {len(listings)} listings ({WORKERS} workers)…')
    found_count = 0
    not_found_count = 0
    completed = 0

    with multiprocessing.Pool(processes=WORKERS, initializer=_worker_init) as pool:
        try:
            for listing, candidate_url, query, skip_reason in pool.imap_unordered(
                _search_listing, listings, chunksize=1
            ):
                completed += 1
                name = listing['name']
                city_slug = listing['city_slug']
                listing_id = listing['id']
                found_url = None

                if candidate_url and not skip_reason:
                    # Duplicate check — safe, main process only
                    if candidate_url in existing_urls:
                        print(f'  ⚠ Duplicate URL, skipping: {candidate_url}')
                        skip_reason = 'duplicate'
                    else:
                        print(f'  ✓ Found: {candidate_url}')
                        found_url = candidate_url
                        found_count += 1
                        existing_urls.add(found_url)
                        output_rows.append({
                                'service': 'dishcult',
                            'name': name,
                            'city': city_slug,
                            'url': found_url,
                        })
                elif not candidate_url and not skip_reason:
                    not_found_count += 1
                    skip_reason = 'not_found'
                    print(f'  — Not found: {name}')
                else:
                    print(f'  — {skip_reason}: {name}')

                log_rows.append({
                    'listing_id': listing_id,
                    'listing_name': name,
                    'listing_city': city_slug,
                    'query': query,
                    'found_url': found_url or '',
                    'skipped_reason': skip_reason,
                })

                if completed % CHECKPOINT_EVERY == 0:
                    print(f'  💾 Checkpoint at {completed} completed…')
                    _save(output_rows, OUTPUT_CSV, FIELDNAMES)
                    _save(log_rows, LOG_CSV, LOG_FIELDNAMES)
                    print(f'  ✓ Saved {len(output_rows)} ResDiary URLs, {len(log_rows)} log entries')

        except KeyboardInterrupt:
            print('\n⚠ Interrupted! Terminating workers…')
            pool.terminate()
            pool.join()
            _save(output_rows, OUTPUT_CSV, FIELDNAMES)
            _save(log_rows, LOG_CSV, LOG_FIELDNAMES)
            print(f'✓ Progress saved: {len(output_rows)} URLs, {len(log_rows)} log entries')
            raise SystemExit(130)

    # ── Final save ────────────────────────────────────────────────────────────
    _save(output_rows, OUTPUT_CSV, FIELDNAMES)
    _save(log_rows, LOG_CSV, LOG_FIELDNAMES)
    print(f'\n{"=" * 60}')
    print(f'✓ Done. {found_count} found, {not_found_count} not found.')
    print(f'✓ Total ResDiary URLs: {len(output_rows)} in {OUTPUT_CSV}')
    print(f'✓ Search log: {len(log_rows)} entries in {LOG_CSV}')
    print('=' * 60)


if __name__ == '__main__':
    main()
