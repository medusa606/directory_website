#!/usr/bin/env python3
"""
enrich_socials.py — Meridian Directory Social Enrichment
=========================================================
Reads an existing CSV of business candidates and enriches social media links
using two strategies:

  1. Deep website crawl (homepage + contact/about/links subpages + JSON-LD)
  2. Search-engine discovery via ddgs (DuckDuckGo/Bing/etc.)

Outputs:
  - An enriched copy of the CSV (non-destructive)
  - A Markdown comparison report showing what changed

Usage:
  python enrich_socials.py meridian_candidates_2026-04-11_172809.csv

Options:
  --max-search N     Max search results per query (default: 5)
  --delay N          Seconds between search queries (default: 2)
  --skip-search      Only do deep website crawl, skip search engine queries
  --skip-crawl       Only do search engine queries, skip deep website crawl
  --verify-urls      Verify discovered URLs return HTTP 200 (slower but fewer dead links)
  --limit N          Only process the first N businesses (for testing)
"""

import argparse
import csv
import logging
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

try:
    from ddgs import DDGS
except ImportError:
    print("ERROR: ddgs package not installed. Run: pip install ddgs")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SOCIAL_COLUMNS = [
    "email",
    "social_facebook",
    "social_instagram",
    "social_twitter",
    "social_tiktok",
    "social_linkedin",
    "social_youtube",
]

# Map from our internal key to CSV column name
KEY_TO_COL = {
    "Email": "email",
    "Social Facebook": "social_facebook",
    "Social Instagram": "social_instagram",
    "Social Twitter": "social_twitter",
    "Social Tiktok": "social_tiktok",
    "Social Linkedin": "social_linkedin",
    "Social Youtube": "social_youtube",
}

# Map from CSV column to search platform keyword
COL_TO_PLATFORM = {
    "social_facebook": "facebook",
    "social_instagram": "instagram",
    "social_twitter": "twitter",
    "social_tiktok": "tiktok",
    "social_linkedin": "linkedin",
    "social_youtube": "youtube",
}

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

# Regex Patterns — improved with exclusion lists for false positives
PATTERNS = {
    "Email": r"(?:mailto:)?([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})",
    "Social Facebook": (
        r"https?://(?:www\.)?facebook\.com/"
        r"(?!sharer|share|tr|flx|plugins|login|recover|help|policies|groups/discover|"
        r"hashtag|watch|marketplace|gaming|events|pages/create|ads|business|"
        r"dialog|v\d)"
        r"([a-zA-Z0-9._/-]+)"
    ),
    "Social Instagram": (
        r"https?://(?:www\.)?instagram\.com/"
        r"(?!explore|accounts|p/|reel/|reels/|stories/|direct|about|developer|legal)"
        r"([a-zA-Z0-9._]+)"
    ),
    "Social Twitter": (
        r"https?://(?:www\.)?(?:twitter\.com|x\.com)/"
        r"(?!intent|share|search|i/|hashtag|home|explore|settings|tos|privacy)"
        r"([a-zA-Z0-9._]+)"
    ),
    "Social Tiktok": r"https?://(?:www\.)?tiktok\.com/@([a-zA-Z0-9._-]+)",
    "Social Linkedin": (
        r"https?://(?:www\.)?linkedin\.com/(?:company|in)/([a-zA-Z0-9._-]+)"
    ),
    "Social Youtube": (
        r"https?://(?:www\.)?youtube\.com/(?:@|c/|channel/|user/)([a-zA-Z0-9._-]+)"
    ),
}

# Known false-positive social handles to reject
FALSE_POSITIVE_HANDLES = {
    "social_facebook": {
        "wordpresscom", "wordpress", "wix", "squarespace", "shopify",
        "2008", "plugins", "sharer.php", "sharer", "profile.php",
        "groups", "watch", "marketplace", "gaming", "events",
        "pages", "ads", "business", "help", "policies",
    },
    "social_instagram": {
        "explore", "accounts", "developer", "about", "legal",
        "p", "reel", "reels", "stories", "direct",
    },
    "social_twitter": {
        "intent", "share", "search", "home", "explore", "i",
        "hashtag", "settings", "tos", "privacy",
    },
    "social_tiktok": set(),
    "social_linkedin": {"company", "in", "pulse", "learning"},
    "social_youtube": {"results", "watch", "playlist"},
}

# Emails that are not real business emails
JUNK_EMAIL_DOMAINS = {
    "example.com", "wixpress.com", "sentry.io", "cloudflare.com",
    "wordpress.com", "squarespace.com", "shopify.com",
    "googleusercontent.com", "gstatic.com",
}

# Subpages likely to contain social links
SOCIAL_SUBPAGES = [
    "/contact", "/contact-us", "/about", "/about-us",
    "/links", "/connect", "/social", "/follow",
]


# ---------------------------------------------------------------------------
# Deep Website Crawl
# ---------------------------------------------------------------------------
def extract_social_and_email_deep(website_url: str, max_pages: int = 5) -> dict:
    """
    Enhanced crawl — homepage + key subpages (contact, about, links).
    Uses BeautifulSoup for link extraction including structured data.
    """
    socials = {k: "" for k in KEY_TO_COL}

    if not website_url:
        return socials

    pages_to_check = [website_url]

    try:
        resp = requests.get(
            website_url, timeout=10, headers=HEADERS, allow_redirects=True
        )
        if resp.status_code != 200:
            return socials

        soup = BeautifulSoup(resp.text, "html.parser")

        # Discover subpages from nav/footer links
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"].lower()
            text = a_tag.get_text(strip=True).lower()
            if any(
                kw in href or kw in text
                for kw in ["contact", "about", "connect", "links", "follow"]
            ):
                full_url = urljoin(website_url, a_tag["href"])
                if urlparse(full_url).netloc == urlparse(website_url).netloc:
                    pages_to_check.append(full_url)

        # Also add standard subpages as fallback
        base = website_url.rstrip("/")
        for subpage in SOCIAL_SUBPAGES:
            pages_to_check.append(f"{base}{subpage}")

        # De-duplicate while preserving order
        seen = set()
        unique_pages = []
        for p in pages_to_check:
            p_norm = p.rstrip("/").lower()
            if p_norm not in seen:
                seen.add(p_norm)
                unique_pages.append(p)

        # Crawl pages (limit to max_pages)
        all_html = ""
        for page_url in unique_pages[:max_pages]:
            try:
                r = requests.get(
                    page_url, timeout=8, headers=HEADERS, allow_redirects=True
                )
                if r.status_code == 200:
                    all_html += r.text + "\n"
            except Exception:
                continue

        # Also extract JSON-LD structured data blocks
        json_ld_blocks = re.findall(
            r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
            all_html,
            re.DOTALL | re.IGNORECASE,
        )
        for block in json_ld_blocks:
            all_html += block

        # Extract socials from combined HTML
        for key, pattern in PATTERNS.items():
            match = re.search(pattern, all_html, re.IGNORECASE)
            if match:
                if key == "Email":
                    email = match.group(1)
                    domain = email.split("@")[-1].lower()
                    if domain not in JUNK_EMAIL_DOMAINS:
                        socials[key] = email
                else:
                    socials[key] = match.group(0)

    except Exception as e:
        log.warning(f"  Deep crawl failed for {website_url}: {e}")

    return socials


# ---------------------------------------------------------------------------
# Name / Query Helpers
# ---------------------------------------------------------------------------
def normalize_name(name: str) -> str:
    """Strip smart quotes, special Unicode chars, and excess whitespace
    so search engines can match the name reliably."""
    # Replace smart quotes / curly apostrophes with nothing or plain equivalent
    name = name.replace("\u2018", "'").replace("\u2019", "'")
    name = name.replace("\u201c", '"').replace("\u201d", '"')
    name = name.replace("\u2013", "-").replace("\u2014", "-")
    # Collapse whitespace
    name = re.sub(r"\s+", " ", name).strip()
    return name


def extract_location(address: str, area_slug: str, city_slug: str) -> str:
    """Build a human-readable location string.
    Prefer the real address field (e.g. 'Easton, Bristol BS5 ...') over slugs."""
    if address:
        # Extract the area/city portion — typically after street number + road
        # e.g. "234 Stapleton Rd, Easton, Bristol BS5 0NT, UK"
        parts = [p.strip() for p in address.split(",")]
        # Take the 2nd and 3rd parts if available (area + city), skip street & postcode/country
        location_parts = []
        for p in parts[1:]:
            clean = p.strip()
            # Stop at postcode or country
            if re.search(r"\b[A-Z]{1,2}\d", clean) or clean.upper() in ("UK", "GB", "UNITED KINGDOM"):
                # But extract city name before postcode if present, e.g. "Bristol BS5 0NT"
                city_match = re.match(r"^([A-Za-z ]+?)\s+[A-Z]{1,2}\d", clean)
                if city_match:
                    location_parts.append(city_match.group(1).strip())
                break
            location_parts.append(clean)
        if location_parts:
            return " ".join(location_parts)
    # Fallback to slugs
    return f"{area_slug} {city_slug}".replace("-", " ").strip()


# ---------------------------------------------------------------------------
# Search-Engine Discovery
# ---------------------------------------------------------------------------
def _do_search(query: str, max_results: int = 5) -> list[dict] | None:
    """Run a ddgs search with rate-limit retry."""
    try:
        return DDGS().text(query, max_results=max_results)
    except Exception as e:
        error_msg = str(e).lower()
        if "ratelimit" in error_msg:
            log.warning(f"  Rate limited on ddgs, backing off 30s...")
            time.sleep(30)
            try:
                return DDGS().text(query, max_results=max_results)
            except Exception:
                log.warning(f"  Rate limited again, skipping: {query}")
                return None
        else:
            log.warning(f"  Search failed for '{query}': {e}")
            return None


def _extract_from_results(results: list[dict], pattern: str, business_name: str = "") -> str | None:
    """Scan search results for a URL matching the given regex pattern.
    If business_name is given, prefer URLs whose handle overlaps with name words."""
    if not results:
        return None

    # Build name-words for relevance scoring
    name_words = set()
    if business_name:
        clean = re.sub(r"[^a-z0-9 ]", "", business_name.lower())
        name_words = {w for w in clean.split() if len(w) > 2}

    candidates = []
    for result in results:
        for text in [result.get("href", ""), result.get("body", "")]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                url = match.group(0)
                handle = match.group(1).lower() if match.lastindex else ""
                # Score: how many business name words appear in the handle
                score = sum(1 for w in name_words if w in handle) if name_words else 0
                candidates.append((score, url))
                break  # one match per result is enough

    if not candidates:
        return None

    # Return the highest-scoring candidate; ties broken by result order (first wins)
    candidates.sort(key=lambda x: -x[0])
    return candidates[0][1]


def search_for_social(
    business_name: str,
    area: str,
    city: str,
    platform: str,
    address: str = "",
    max_results: int = 5,
) -> str | None:
    """
    Search for a business's social media profile using ddgs.
    Tries a quoted query first, then falls back to an unquoted broader query.
    Returns the first matching social URL or None.
    """
    clean_name = normalize_name(business_name)
    location = extract_location(address, area, city)

    # Determine which pattern to look for
    platform_to_key = {
        "facebook": "Social Facebook",
        "instagram": "Social Instagram",
        "twitter": "Social Twitter",
        "tiktok": "Social Tiktok",
        "linkedin": "Social Linkedin",
        "youtube": "Social Youtube",
    }
    key = platform_to_key.get(platform)
    if not key or key not in PATTERNS:
        return None
    pattern = PATTERNS[key]

    # Strategy 1: Quoted name + location (precise)
    query1 = f'"{clean_name}" {location} {platform}'
    results = _do_search(query1, max_results=max_results)
    found = _extract_from_results(results, pattern, clean_name)
    if found:
        return found

    # Strategy 2: Unquoted, simpler query (broader — catches partial matches)
    # Strip apostrophes entirely for better matching
    simple_name = re.sub(r"['\"-]", "", clean_name)
    query2 = f"{simple_name} {location} {platform}"
    if query2 != query1:
        time.sleep(1)  # brief pause between retries
        results = _do_search(query2, max_results=max_results)
        found = _extract_from_results(results, pattern, clean_name)
        if found:
            return found

    # Strategy 3: site: search — directly search on the platform's domain
    # This catches cases where the other engines don't rank the profile page
    PLATFORM_DOMAINS = {
        "facebook": "facebook.com",
        "instagram": "instagram.com",
        "twitter": "twitter.com OR site:x.com",
        "tiktok": "tiktok.com",
        "linkedin": "linkedin.com",
        "youtube": "youtube.com",
    }
    domain = PLATFORM_DOMAINS.get(platform)
    if domain:
        query3 = f"{simple_name} {location} site:{domain}"
        time.sleep(1)
        results = _do_search(query3, max_results=max_results)
        found = _extract_from_results(results, pattern, clean_name)
        if found:
            return found

    return None


def search_tiktok_mentions(
    business_name: str, area: str, city: str, address: str = "",
    max_results: int = 5,
) -> list[str]:
    """
    Search for TikTok videos mentioning a business (not just their own account).
    Returns a list of TikTok video URLs.
    """
    clean_name = normalize_name(business_name)
    location = extract_location(address, area, city)
    query = f'{clean_name} {location} site:tiktok.com'

    results = _do_search(query, max_results=max_results)

    tiktok_urls = []
    if results:
        for r in results:
            href = r.get("href", "")
            # Only keep actual video/profile URLs, not /discover/ or /tag/ pages
            if "tiktok.com" in href and (
                "/video/" in href
                or "tiktok.com/@" in href
            ) and "/discover/" not in href:
                tiktok_urls.append(href)

    return tiktok_urls


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------
def is_valid_social_url(col: str, url: str) -> bool:
    """Check if a discovered social URL looks legitimate (not a false positive)."""
    if not url:
        return False

    url_lower = url.lower().rstrip("/")

    # Check against known false positive handles
    bad_handles = FALSE_POSITIVE_HANDLES.get(col, set())
    for bad in bad_handles:
        if url_lower.endswith(f"/{bad}") or url_lower.endswith(f"/{bad}/"):
            return False

    # Reject URLs that are just the platform root
    parsed = urlparse(url_lower)
    path = parsed.path.strip("/")
    if not path or path in ("", "/"):
        return False

    # Facebook-specific: reject profile.php, groups, photos, posts links
    if col == "social_facebook":
        if any(seg in path for seg in [
            "profile.php", "/groups/", "/photos/", "/posts/",
            "/people/", "/884343",  # numeric-only IDs are usually junk
        ]):
            # Allow /people/ pages that look like real business pages
            if "/people/" in path and len(path.split("/")) >= 3:
                pass  # these are OK: facebook.com/people/Business-Name/12345
            elif "profile.php" in path:
                return False
            elif "/groups/" in path or "/photos/" in path or "/posts/" in path:
                return False

    return True


def is_valid_email(email: str) -> bool:
    """Check if an email looks like a real business email."""
    if not email:
        return False
    domain = email.split("@")[-1].lower()
    return domain not in JUNK_EMAIL_DOMAINS


def verify_url_exists(url: str) -> bool:
    """Check if a URL actually returns HTTP 200 (optional verification)."""
    try:
        resp = requests.head(
            url, timeout=8, headers=HEADERS, allow_redirects=True
        )
        return resp.status_code < 400
    except Exception:
        return False


# ---------------------------------------------------------------------------
# Main Enrichment Pipeline
# ---------------------------------------------------------------------------
def enrich_csv(
    input_csv: str,
    max_search: int = 5,
    delay: float = 2.0,
    skip_search: bool = False,
    skip_crawl: bool = False,
    do_verify: bool = False,
    limit: int | None = None,
):
    """Main enrichment pipeline."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base = os.path.splitext(os.path.basename(input_csv))[0]
    output_csv = f"{base}_enriched_{timestamp}.csv"
    report_file = f"enrichment_report_{timestamp}.md"

    # Read CSV
    with open(input_csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        rows = list(reader)

    if not fieldnames:
        log.error("CSV has no headers")
        return

    # Add tiktok_mentions column if not present
    if "tiktok_mentions" not in fieldnames:
        fieldnames = list(fieldnames) + ["tiktok_mentions"]

    total = len(rows)
    if limit:
        rows_to_process = rows[:limit]
        log.info(f"Processing {limit} of {total} businesses (--limit)")
    else:
        rows_to_process = rows
        log.info(f"Processing all {total} businesses")

    # Track changes for report
    changes = []  # list of dicts: {name, column, original, new_value, source}

    # Before-counts
    before_counts = {}
    for col in SOCIAL_COLUMNS:
        before_counts[col] = sum(1 for r in rows if r.get(col, "").strip())

    for idx, row in enumerate(rows_to_process):
        name = row.get("name", "Unknown")
        area = row.get("area_slug", "")
        city = row.get("city_slug", "")
        address = row.get("address", "")
        website = row.get("website", "").strip()
        chain = row.get("chain_flag", "").lower() == "true"

        log.info(f"[{idx+1}/{len(rows_to_process)}] {name}")

        if chain:
            log.info(f"  Skipping chain business")
            continue

        # ------------------------------------------------------------------
        # Phase 1: Deep website crawl
        # ------------------------------------------------------------------
        crawl_results = {}
        if not skip_crawl and website:
            log.info(f"  Deep crawling website: {website}")
            crawl_results = extract_social_and_email_deep(website)
            time.sleep(1)  # polite delay

        # ------------------------------------------------------------------
        # Phase 2: Search engine discovery for missing socials
        # ------------------------------------------------------------------
        search_results = {}
        if not skip_search:
            for col, platform in COL_TO_PLATFORM.items():
                # Skip if we already have a valid value (original or crawled)
                existing = row.get(col, "").strip()
                crawled_key = [k for k, v in KEY_TO_COL.items() if v == col][0]
                crawled_val = crawl_results.get(crawled_key, "").strip()

                if existing and is_valid_social_url(col, existing):
                    continue
                if crawled_val and is_valid_social_url(col, crawled_val):
                    continue

                log.info(f"  Searching for {platform}...")
                found = search_for_social(
                    name, area, city, platform,
                    address=address, max_results=max_search,
                )
                if found:
                    search_results[col] = found
                    log.info(f"    Found: {found}")

                time.sleep(delay)

            # Also search for email if missing — but only accept if domain
            # plausibly relates to the business (search results are noisy)
            existing_email = row.get("email", "").strip()
            crawled_email = crawl_results.get("Email", "").strip()
            if not existing_email and not crawled_email:
                log.info(f"  Searching for email...")
                clean_name = normalize_name(name)
                location = extract_location(address, area, city)
                try:
                    results = _do_search(
                        f'{clean_name} {location} email contact',
                        max_results=max_search,
                    )
                    if results:
                        # Build a set of name-words to match against email domains
                        name_words = set(
                            re.sub(r"[^a-z0-9 ]", "", name.lower()).split()
                        )
                        for r in results:
                            body = r.get("body", "") + " " + r.get("href", "")
                            match = re.search(PATTERNS["Email"], body, re.IGNORECASE)
                            if match:
                                email_found = match.group(1)
                                if is_valid_email(email_found):
                                    # Check domain has some word overlap with business name
                                    domain = email_found.split("@")[-1].split(".")[0].lower()
                                    if any(w in domain for w in name_words if len(w) > 2):
                                        search_results["email"] = email_found
                                        log.info(f"    Found email: {email_found}")
                                        break
                                    else:
                                        log.info(f"    Skipping unrelated email: {email_found}")
                except Exception:
                    pass
                time.sleep(delay)

            # Search for TikTok mentions (videos about the business)
            log.info(f"  Searching for TikTok mentions...")
            tiktok_mentions = search_tiktok_mentions(
                name, area, city, address=address,
            )
            if tiktok_mentions:
                row["tiktok_mentions"] = " | ".join(tiktok_mentions[:3])
                log.info(f"    Found {len(tiktok_mentions)} TikTok mention(s)")
            time.sleep(delay)

        # ------------------------------------------------------------------
        # Phase 3: Merge results (never overwrite valid existing data)
        # ------------------------------------------------------------------
        for key, col in KEY_TO_COL.items():
            original = row.get(col, "").strip()
            crawled = crawl_results.get(key, "").strip()
            searched = search_results.get(col, "").strip()

            # Determine the best new value
            new_value = ""
            source = ""

            if col == "email":
                if crawled and is_valid_email(crawled):
                    new_value = crawled
                    source = "deep_crawl"
                elif searched and is_valid_email(searched):
                    new_value = searched
                    source = "search"
            else:
                if crawled and is_valid_social_url(col, crawled):
                    new_value = crawled
                    source = "deep_crawl"
                elif searched and is_valid_social_url(col, searched):
                    new_value = searched
                    source = "search"

            # Optional URL verification
            if do_verify and new_value and col != "email":
                if not verify_url_exists(new_value):
                    log.info(f"    URL verification failed: {new_value}")
                    new_value = ""
                    source = ""

            # Only update if we have a new value and original is empty/invalid
            if new_value:
                if not original:
                    row[col] = new_value
                    changes.append({
                        "name": name,
                        "column": col,
                        "original": original,
                        "new_value": new_value,
                        "source": source,
                        "status": "NEW",
                    })
                elif col != "email" and not is_valid_social_url(col, original):
                    # Original was invalid — replace it
                    changes.append({
                        "name": name,
                        "column": col,
                        "original": original,
                        "new_value": new_value,
                        "source": source,
                        "status": "REPLACED",
                    })
                    row[col] = new_value

    # ------------------------------------------------------------------
    # Write enriched CSV
    # ------------------------------------------------------------------
    with open(output_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    log.info(f"Enriched CSV written to: {output_csv}")

    # ------------------------------------------------------------------
    # After-counts
    # ------------------------------------------------------------------
    after_counts = {}
    for col in SOCIAL_COLUMNS:
        after_counts[col] = sum(1 for r in rows if r.get(col, "").strip())

    # ------------------------------------------------------------------
    # Generate Report
    # ------------------------------------------------------------------
    report_lines = []
    report_lines.append(f"# Social Enrichment Report")
    report_lines.append(f"")
    report_lines.append(f"**Source CSV**: `{input_csv}`")
    report_lines.append(f"**Enriched CSV**: `{output_csv}`")
    report_lines.append(f"**Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append(f"**Businesses processed**: {len(rows_to_process)} of {total}")
    report_lines.append(f"")

    # Summary stats
    report_lines.append(f"## Summary — Fill Rates Before / After")
    report_lines.append(f"")
    report_lines.append(f"| Field | Before | After | New Finds |")
    report_lines.append(f"|-------|--------|-------|-----------|")
    total_new = 0
    for col in SOCIAL_COLUMNS:
        before = before_counts[col]
        after = after_counts[col]
        diff = after - before
        total_new += diff
        report_lines.append(f"| {col} | {before}/{total} | {after}/{total} | +{diff} |")
    report_lines.append(f"| **TOTAL** | | | **+{total_new}** |")
    report_lines.append(f"")

    # Per-business changes
    if changes:
        report_lines.append(f"## Changes by Business")
        report_lines.append(f"")
        report_lines.append(f"| Business | Field | Original | New Value | Source | Status |")
        report_lines.append(f"|----------|-------|----------|-----------|--------|--------|")
        for c in sorted(changes, key=lambda x: x["name"]):
            orig_display = c["original"] if c["original"] else "*(empty)*"
            report_lines.append(
                f"| {c['name']} | {c['column']} | {orig_display} | {c['new_value']} | {c['source']} | {c['status']} |"
            )
        report_lines.append(f"")
    else:
        report_lines.append(f"## Changes by Business")
        report_lines.append(f"")
        report_lines.append(f"*No new social links were discovered.*")
        report_lines.append(f"")

    # TikTok mentions section
    tiktok_mention_rows = [r for r in rows if r.get("tiktok_mentions", "").strip()]
    if tiktok_mention_rows:
        report_lines.append(f"## TikTok Mentions (videos about these businesses)")
        report_lines.append(f"")
        report_lines.append(f"| Business | TikTok Video URLs |")
        report_lines.append(f"|----------|-------------------|")
        for r in tiktok_mention_rows:
            report_lines.append(f"| {r['name']} | {r['tiktok_mentions']} |")
        report_lines.append(f"")

    report_text = "\n".join(report_lines)

    with open(report_file, "w", encoding="utf-8") as f:
        f.write(report_text)

    log.info(f"Report written to: {report_file}")

    # Also print summary to console
    print("\n" + "=" * 60)
    print("ENRICHMENT COMPLETE")
    print("=" * 60)
    print(f"Businesses processed: {len(rows_to_process)}")
    print(f"Total new social links found: {total_new}")
    print(f"Total changes: {len(changes)}")
    print()
    for col in SOCIAL_COLUMNS:
        before = before_counts[col]
        after = after_counts[col]
        diff = after - before
        if diff > 0:
            print(f"  {col}: {before} → {after} (+{diff})")
        else:
            print(f"  {col}: {before} → {after}")
    print()
    print(f"Enriched CSV: {output_csv}")
    print(f"Report: {report_file}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Enrich business CSV with social media links"
    )
    parser.add_argument("csv_file", help="Input CSV file to enrich")
    parser.add_argument(
        "--max-search", type=int, default=5,
        help="Max search results per query (default: 5)",
    )
    parser.add_argument(
        "--delay", type=float, default=2.0,
        help="Seconds between search queries (default: 2)",
    )
    parser.add_argument(
        "--skip-search", action="store_true",
        help="Skip search engine queries (deep crawl only)",
    )
    parser.add_argument(
        "--skip-crawl", action="store_true",
        help="Skip deep website crawl (search only)",
    )
    parser.add_argument(
        "--verify-urls", action="store_true",
        help="Verify discovered URLs return HTTP 200",
    )
    parser.add_argument(
        "--limit", type=int, default=None,
        help="Only process first N businesses (for testing)",
    )

    args = parser.parse_args()

    if not os.path.exists(args.csv_file):
        print(f"ERROR: File not found: {args.csv_file}")
        sys.exit(1)

    enrich_csv(
        input_csv=args.csv_file,
        max_search=args.max_search,
        delay=args.delay,
        skip_search=args.skip_search,
        skip_crawl=args.skip_crawl,
        do_verify=args.verify_urls,
        limit=args.limit,
    )


if __name__ == "__main__":
    main()
