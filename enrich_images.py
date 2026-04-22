"""
enrich_images.py — Scrape business websites for hero and logo images.

No paid API required. Uses og:image, twitter:image, Schema.org JSON-LD,
apple-touch-icon, favicons, and img tag heuristics.

For each business with a website:
  - Fetches the HTML (10s timeout)
  - Extracts all candidate images with source labels
  - Makes a best-guess for hero and logo
  - Updates photo_url / logo_url in baseline.csv (in-place)
  - Writes image_candidates.json for the curation UI
  - Generates image_curator.html (self-contained, file:// ready)

Usage:
    python enrich_images.py [--file baseline.csv] [--limit 50] [--skip-existing]
"""

import argparse
import json
import logging
import os
import re
import sys
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import pandas as pd
import requests
from bs4 import BeautifulSoup

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5   # seconds between requests, be polite
MAX_IMG_CANDIDATES = 20

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; MeridianDirectoryBot/1.0; "
        "+https://meridian.directory/about)"
    )
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Image extraction
# ---------------------------------------------------------------------------

def _abs(url: str, base: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if url.startswith("data:"):
        return ""       # skip inline data URIs
    return urljoin(base, url)


def extract_candidates(html: str, base_url: str) -> list[dict]:
    """
    Return ordered list of image candidate dicts:
      { url, source, priority, alt }
    Lower priority number = higher confidence.
    """
    soup = BeautifulSoup(html, "lxml")
    candidates = []

    def add(url, source, priority, alt=""):
        url = _abs(url, base_url)
        if url and not url.startswith("data:"):
            candidates.append({"url": url, "source": source, "priority": priority, "alt": alt})

    # --- og:image ---
    for tag in soup.find_all("meta", property="og:image"):
        add(tag.get("content", ""), "og:image", 1)
    for tag in soup.find_all("meta", attrs={"name": "og:image"}):
        add(tag.get("content", ""), "og:image", 1)
    # og:image:secure_url
    for tag in soup.find_all("meta", property="og:image:secure_url"):
        add(tag.get("content", ""), "og:image:secure_url", 2)

    # --- twitter:image ---
    for tag in soup.find_all("meta", attrs={"name": "twitter:image"}):
        add(tag.get("content", ""), "twitter:image", 3)
    for tag in soup.find_all("meta", property="twitter:image"):
        add(tag.get("content", ""), "twitter:image", 3)

    # --- Schema.org JSON-LD: Organization.logo / ImageObject ---
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            data = json.loads(script.string or "")
            # may be a list of schemas
            items = data if isinstance(data, list) else [data]
            for item in items:
                # handle @graph
                if not isinstance(item, dict):
                    continue
                if "@graph" in item:
                    items.extend(item["@graph"])
                logo = item.get("logo")
                if isinstance(logo, str):
                    add(logo, "schema.org/logo", 4)
                elif isinstance(logo, dict):
                    add(logo.get("url", "") or logo.get("contentUrl", ""), "schema.org/logo", 4)
                image = item.get("image")
                if isinstance(image, str):
                    add(image, "schema.org/image", 5)
                elif isinstance(image, dict):
                    add(image.get("url", "") or image.get("contentUrl", ""), "schema.org/image", 5)
                elif isinstance(image, list):
                    for img in image:
                        if isinstance(img, str):
                            add(img, "schema.org/image", 5)
                        elif isinstance(img, dict):
                            add(img.get("url", "") or img.get("contentUrl", ""), "schema.org/image", 5)
        except (json.JSONDecodeError, AttributeError):
            pass

    # --- apple-touch-icon ---
    for rel in ["apple-touch-icon", "apple-touch-icon-precomposed"]:
        for tag in soup.find_all("link", rel=rel):
            add(tag.get("href", ""), "apple-touch-icon", 6)

    # --- favicon ---
    for tag in soup.find_all("link", rel=lambda r: r and "icon" in r):
        href = tag.get("href", "")
        # skip SVG favicons for now (often too small/stylised)
        if href and not href.endswith(".svg"):
            add(href, "favicon", 8)

    # --- <img> tags with "logo" in src/alt/class/id ---
    for tag in soup.find_all("img"):
        src = tag.get("src", "") or tag.get("data-src", "") or tag.get("data-lazy-src", "")
        alt = tag.get("alt", "")
        classes = " ".join(tag.get("class", []))
        img_id = tag.get("id", "")
        is_logo = any(
            "logo" in x.lower()
            for x in [src, alt, classes, img_id]
        )
        if is_logo:
            add(src, "img[logo]", 7, alt)

    # --- large <img> tags (hero candidates) ---
    for tag in soup.find_all("img"):
        src = tag.get("src", "") or tag.get("data-src", "") or tag.get("data-lazy-src", "")
        if not src:
            continue
        alt = tag.get("alt", "")
        width = tag.get("width", "")
        height = tag.get("height", "")
        try:
            w = int(str(width).replace("px", ""))
        except (ValueError, TypeError):
            w = 0
        # only include images with explicit large width or no size hints (could be responsive)
        if w >= 400 or (w == 0 and not str(src).endswith((".ico", ".gif"))):
            add(src, "img", 9, alt)

    # Deduplicate by URL, keeping lowest priority
    seen = {}
    for c in candidates:
        u = c["url"]
        if u not in seen or c["priority"] < seen[u]["priority"]:
            seen[u] = c

    result = sorted(seen.values(), key=lambda x: x["priority"])
    return result[:MAX_IMG_CANDIDATES]


def best_guess_hero(candidates: list[dict]) -> str:
    for source in ["og:image", "og:image:secure_url", "twitter:image", "schema.org/image"]:
        for c in candidates:
            if c["source"] == source:
                return c["url"]
    # fallback: any large img
    for c in candidates:
        if c["source"] == "img":
            return c["url"]
    return ""


def best_guess_logo(candidates: list[dict]) -> str:
    for source in ["schema.org/logo", "img[logo]", "apple-touch-icon"]:
        for c in candidates:
            if c["source"] == source:
                return c["url"]
    # favicon as last resort
    for c in candidates:
        if c["source"] == "favicon":
            return c["url"]
    return ""


# ---------------------------------------------------------------------------
# HTTP fetch
# ---------------------------------------------------------------------------

def fetch_website(url: str) -> str | None:
    """Fetch URL, follow redirects, return HTML string or None."""
    if not url:
        return None
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT, allow_redirects=True)
        if resp.status_code == 200:
            return resp.text
        logger.debug(f"  HTTP {resp.status_code} for {url}")
    except requests.RequestException as exc:
        logger.debug(f"  Fetch error for {url}: {exc}")
    return None


# ---------------------------------------------------------------------------
# Main enrichment
# ---------------------------------------------------------------------------

def run(csv_path: str, limit: int | None, skip_existing: bool):
    df = pd.read_csv(csv_path, dtype=str, keep_default_na=False)

    # Ensure columns exist
    for col in ["photo_url", "logo_url", "google_photo_reference"]:
        if col not in df.columns:
            df[col] = ""

    records = []  # for image_candidates.json

    total = 0
    enriched = 0

    for idx, row in df.iterrows():
        website = str(row.get("website", "")).strip()
        if not website:
            continue

        if skip_existing:
            has_photo = str(row.get("photo_url", "")).strip() not in ("", "nan", "none")
            has_logo = str(row.get("logo_url", "")).strip() not in ("", "nan", "none")
            if has_photo and has_logo:
                records.append({
                    "business_slug": row.get("business_slug", ""),
                    "name": row.get("name", ""),
                    "address": row.get("address", ""),
                    "website": website,
                    "candidates": [],
                    "guess_hero": str(row.get("photo_url", "")),
                    "guess_logo": str(row.get("logo_url", "")),
                    "selected_hero": str(row.get("photo_url", "")),
                    "selected_logo": str(row.get("logo_url", "")),
                })
                continue

        total += 1
        if limit and total > limit:
            break

        logger.info(f"[{total}] {row.get('name', '?')} — {website}")

        html = fetch_website(website)
        if not html:
            records.append({
                "business_slug": row.get("business_slug", ""),
                "name": row.get("name", ""),
                "address": row.get("address", ""),
                "website": website,
                "candidates": [],
                "guess_hero": "",
                "guess_logo": "",
                "selected_hero": "",
                "selected_logo": "",
            })
            time.sleep(REQUEST_DELAY)
            continue

        # Normalise base_url
        parsed = urlparse(website if website.startswith("http") else "https://" + website)
        base_url = f"{parsed.scheme}://{parsed.netloc}"

        candidates = extract_candidates(html, base_url)
        hero = best_guess_hero(candidates)
        logo = best_guess_logo(candidates)

        # Write guesses back to CSV
        if hero:
            df.at[idx, "photo_url"] = hero
        if logo:
            df.at[idx, "logo_url"] = logo

        records.append({
            "business_slug": row.get("business_slug", ""),
            "name": row.get("name", ""),
            "address": row.get("address", ""),
            "website": website,
            "candidates": candidates,
            "guess_hero": hero,
            "guess_logo": logo,
            "selected_hero": hero,
            "selected_logo": logo,
        })

        enriched += 1
        time.sleep(REQUEST_DELAY)

    # Save CSV in place
    df.to_csv(csv_path, index=False)
    logger.info(f"CSV updated in place: {csv_path}  ({enriched} rows enriched)")

    # Save JSON
    json_path = Path(csv_path).parent / "image_candidates.json"
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    logger.info(f"Candidates JSON: {json_path}")

    # Generate curator HTML
    html_path = Path(csv_path).parent / "image_curator.html"
    generate_curator_html(records, html_path, csv_path)
    logger.info(f"Curator HTML: {html_path}")


# ---------------------------------------------------------------------------
# Curator HTML generator
# ---------------------------------------------------------------------------

CURATOR_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Image Curator — Meridian Directory</title>
<style>
  *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
  body { font-family: system-ui, -apple-system, sans-serif; background: #f2f4f7; color: #222; }
  header { background: #1a1a2e; color: #fff; padding: 14px 24px; display: flex; align-items: center; gap: 16px; position: sticky; top: 0; z-index: 100; }
  header h1 { font-size: 1.1rem; font-weight: 600; flex: 1; }
  .page-nav { display: flex; align-items: center; gap: 12px; }
  .page-nav button { background: #fff2; border: 1px solid #fff3; color: #fff; padding: 6px 14px; border-radius: 6px; cursor: pointer; font-size: 0.85rem; }
  .page-nav button:hover { background: #fff3; }
  .page-nav button:disabled { opacity: 0.35; cursor: default; }
  .page-label { font-size: 0.9rem; color: #ccd; min-width: 180px; text-align: center; }

  .toolbar { background: #fff; border-bottom: 1px solid #e0e0e0; padding: 10px 24px; display: flex; align-items: center; gap: 12px; }
  .toolbar button { padding: 7px 16px; border-radius: 7px; border: none; cursor: pointer; font-size: 0.85rem; font-weight: 600; }
  #btn-export { background: #1e8c45; color: #fff; }
  #btn-export:hover { background: #166b34; }
  #btn-clear-all { background: #e5e7eb; color: #555; }
  #btn-clear-all:hover { background: #d1d5db; }
  .saved-status { font-size: 0.8rem; color: #888; margin-left: auto; }

  .listings-grid { padding: 20px 24px; display: flex; flex-direction: column; gap: 24px; }

  /* Listing card */
  .listing-card { background: #fff; border-radius: 12px; box-shadow: 0 1px 4px rgba(0,0,0,0.08); overflow: hidden; }
  .listing-header { padding: 14px 18px 10px; border-bottom: 1px solid #f0f0f0; display: flex; justify-content: space-between; align-items: flex-start; gap: 12px; }
  .listing-info h2 { font-size: 1rem; font-weight: 700; margin-bottom: 2px; }
  .listing-info .address { font-size: 0.8rem; color: #666; }
  .listing-info a { font-size: 0.78rem; color: #2563eb; text-decoration: none; }
  .listing-info a:hover { text-decoration: underline; }
  .listing-status { font-size: 0.75rem; padding: 4px 10px; border-radius: 20px; white-space: nowrap; }
  .status-both { background: #d1fae5; color: #065f46; }
  .status-partial { background: #fef3c7; color: #92400e; }
  .status-none { background: #fee2e2; color: #991b1b; }

  .images-area { padding: 12px 18px 16px; }
  .no-images { font-size: 0.85rem; color: #999; padding: 8px 0; }

  .img-grid { display: flex; flex-wrap: wrap; gap: 12px; }
  .img-card { position: relative; border: 3px solid transparent; border-radius: 10px; overflow: hidden; cursor: pointer; width: 148px; flex-shrink: 0; background: #f8f9fa; transition: border-color 0.15s, box-shadow 0.15s; }
  .img-card:hover { box-shadow: 0 2px 8px rgba(0,0,0,0.15); }
  .img-card.hero  { border-color: #2563eb; box-shadow: 0 0 0 2px #93c5fd; }
  .img-card.logo  { border-color: #16a34a; box-shadow: 0 0 0 2px #86efac; }
  .img-card.hero.logo { border-color: #7c3aed; box-shadow: 0 0 0 2px #c4b5fd; }
  .img-card img { width: 148px; height: 110px; object-fit: cover; display: block; background: #e5e7eb; }
  .img-card .img-meta { padding: 5px 6px; font-size: 0.7rem; }
  .source-badge { display: inline-block; background: #e0e7ff; color: #3730a3; padding: 1px 6px; border-radius: 4px; font-size: 0.65rem; font-weight: 600; margin-bottom: 3px; }
  .img-alt { color: #666; overflow: hidden; white-space: nowrap; text-overflow: ellipsis; max-width: 136px; }

  .btn-row { display: flex; gap: 6px; padding: 4px 6px 6px; }
  .btn-tag { flex: 1; font-size: 0.7rem; font-weight: 700; border: none; border-radius: 5px; padding: 4px 2px; cursor: pointer; transition: background 0.1s; }
  .btn-hero { background: #dbeafe; color: #1d4ed8; }
  .btn-hero.active { background: #2563eb; color: #fff; }
  .btn-hero:hover:not(.active) { background: #bfdbfe; }
  .btn-logo { background: #dcfce7; color: #15803d; }
  .btn-logo.active { background: #16a34a; color: #fff; }
  .btn-logo:hover:not(.active) { background: #bbf7d0; }

  footer { text-align: center; padding: 24px; font-size: 0.8rem; color: #999; }
</style>
</head>
<body>

<header>
  <h1>🖼 Image Curator — Meridian Directory</h1>
  <div class="page-nav">
    <button id="btn-prev" onclick="changePage(-1)" disabled>← Prev</button>
    <span class="page-label" id="page-label">Page 1</span>
    <button id="btn-next" onclick="changePage(1)">Next →</button>
  </div>
</header>

<div class="toolbar">
  <button id="btn-export" onclick="exportCSV()">⬇ Export CSV</button>
  <button id="btn-clear-all" onclick="if(confirm('Clear all selections on this page?')) clearPage()">Clear Page</button>
  <span class="saved-status" id="save-status">Selections auto-saved in browser</span>
</div>

<div class="listings-grid" id="listings-grid"></div>

<footer>
  Use the Hero 🔵 and Logo 🟢 buttons to select images. Selections are saved in localStorage. Click Export CSV when done.
</footer>

<script>
const DATA = __DATA_PLACEHOLDER__;
const PAGE_SIZE = 20;
let currentPage = 0;
const totalPages = Math.ceil(DATA.length / PAGE_SIZE);

const STORE_KEY = 'meridian_image_selections';

function loadSelections() {
  try {
    return JSON.parse(localStorage.getItem(STORE_KEY) || '{}');
  } catch { return {}; }
}

function saveSelections(selections) {
  localStorage.setItem(STORE_KEY, JSON.stringify(selections));
  document.getElementById('save-status').textContent = 'Saved ' + new Date().toLocaleTimeString();
}

function getSelections() {
  return loadSelections();
}

function setSelection(slug, type, url) {
  const sel = loadSelections();
  if (!sel[slug]) sel[slug] = { hero: '', logo: '' };
  sel[slug][type] = url;
  saveSelections(sel);
}

function clearUrl(slug, type) {
  const sel = loadSelections();
  if (sel[slug]) sel[slug][type] = '';
  saveSelections(sel);
}

function renderPage() {
  const start = currentPage * PAGE_SIZE;
  const end = Math.min(start + PAGE_SIZE, DATA.length);
  const items = DATA.slice(start, end);
  const sel = getSelections();
  const grid = document.getElementById('listings-grid');
  grid.innerHTML = '';

  items.forEach((listing, li) => {
    const slug = listing.business_slug || ('item_' + (start + li));
    const current = sel[slug] || { hero: listing.selected_hero || '', logo: listing.selected_logo || '' };

    // Initialise from guess if not yet set
    if (current.hero === undefined) current.hero = listing.selected_hero || '';
    if (current.logo === undefined) current.logo = listing.selected_logo || '';

    const heroUrl = current.hero;
    const logoUrl = current.logo;

    const hasHero = heroUrl && heroUrl.trim();
    const hasLogo = logoUrl && logoUrl.trim();
    const statusClass = hasHero && hasLogo ? 'status-both' : (hasHero || hasLogo ? 'status-partial' : 'status-none');
    const statusText = hasHero && hasLogo ? '✓ Hero + Logo' : hasHero ? '◑ Hero only' : hasLogo ? '◑ Logo only' : '✗ No selection';

    let imagesHtml = '';
    if (listing.candidates && listing.candidates.length > 0) {
      listing.candidates.forEach((img, ci) => {
        const isHero = img.url === heroUrl;
        const isLogo = img.url === logoUrl;
        const cardClass = [isHero ? 'hero' : '', isLogo ? 'logo' : ''].filter(Boolean).join(' ');
        const altText = img.alt ? img.alt.substring(0, 30) : '';
        imagesHtml += `
          <div class="img-card ${cardClass}" id="card-${slug}-${ci}" data-url="${escHtml(img.url)}" data-slug="${escHtml(slug)}">
            <img src="${escHtml(img.url)}" alt="${escHtml(altText)}" loading="lazy" onerror="this.style.display='none'">
            <div class="img-meta">
              <span class="source-badge">${escHtml(img.source)}</span>
              <div class="img-alt">${escHtml(altText || img.url.split('/').pop().substring(0,30))}</div>
            </div>
            <div class="btn-row">
              <button class="btn-tag btn-hero ${isHero ? 'active' : ''}" onclick="selectImage(event, '${escHtml(slug)}','hero','${escHtml(img.url)}')">HERO</button>
              <button class="btn-tag btn-logo ${isLogo ? 'active' : ''}" onclick="selectImage(event, '${escHtml(slug)}','logo','${escHtml(img.url)}')">LOGO</button>
            </div>
          </div>`;
      });
    } else {
      imagesHtml = '<p class="no-images">No images found for this website.</p>';
    }

    const websiteHtml = listing.website
      ? `<a href="${escHtml(listing.website)}" target="_blank" rel="noopener">${escHtml(listing.website)}</a>`
      : '';

    grid.insertAdjacentHTML('beforeend', `
      <div class="listing-card" id="listing-${escHtml(slug)}">
        <div class="listing-header">
          <div class="listing-info">
            <h2>${escHtml(listing.name || 'Unknown')}</h2>
            <div class="address">${escHtml(listing.address || '')}</div>
            ${websiteHtml}
          </div>
          <span class="listing-status ${statusClass}" id="status-${escHtml(slug)}">${statusText}</span>
        </div>
        <div class="images-area">
          <div class="img-grid">${imagesHtml}</div>
        </div>
      </div>`);
  });

  // Update pagination controls
  document.getElementById('page-label').textContent =
    `Page ${currentPage + 1} of ${totalPages} · listings ${start + 1}–${end}`;
  document.getElementById('btn-prev').disabled = currentPage === 0;
  document.getElementById('btn-next').disabled = currentPage >= totalPages - 1;
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

function selectImage(event, slug, type, url) {
  event.stopPropagation();
  const sel = loadSelections();
  if (!sel[slug]) sel[slug] = { hero: '', logo: '' };
  // Toggle off if already selected
  if (sel[slug][type] === url) {
    sel[slug][type] = '';
  } else {
    sel[slug][type] = url;
  }
  saveSelections(sel);

  // Re-render just this listing's cards efficiently
  const start = currentPage * PAGE_SIZE;
  const listing = DATA.find(d => (d.business_slug || '') === slug);
  if (!listing || !listing.candidates) return;

  const heroUrl = sel[slug].hero || '';
  const logoUrl = sel[slug].logo || '';

  listing.candidates.forEach((img, ci) => {
    const card = document.getElementById(`card-${slug}-${ci}`);
    if (!card) return;
    const isHero = img.url === heroUrl;
    const isLogo = img.url === logoUrl;
    card.className = 'img-card ' + [isHero ? 'hero' : '', isLogo ? 'logo' : ''].filter(Boolean).join(' ');
    card.querySelectorAll('.btn-hero').forEach(b => b.classList.toggle('active', isHero));
    card.querySelectorAll('.btn-logo').forEach(b => b.classList.toggle('active', isLogo));
  });

  // Update status badge
  const badge = document.getElementById(`status-${slug}`);
  if (badge) {
    const hasHero = heroUrl.trim() !== '';
    const hasLogo = logoUrl.trim() !== '';
    badge.className = 'listing-status ' + (hasHero && hasLogo ? 'status-both' : (hasHero || hasLogo ? 'status-partial' : 'status-none'));
    badge.textContent = hasHero && hasLogo ? '✓ Hero + Logo' : hasHero ? '◑ Hero only' : hasLogo ? '◑ Logo only' : '✗ No selection';
  }
}

function changePage(dir) {
  currentPage = Math.max(0, Math.min(totalPages - 1, currentPage + dir));
  renderPage();
}

function clearPage() {
  const start = currentPage * PAGE_SIZE;
  const end = Math.min(start + PAGE_SIZE, DATA.length);
  const sel = loadSelections();
  DATA.slice(start, end).forEach(listing => {
    const slug = listing.business_slug;
    if (slug && sel[slug]) { sel[slug].hero = ''; sel[slug].logo = ''; }
  });
  saveSelections(sel);
  renderPage();
}

function escHtml(str) {
  return String(str || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

function exportCSV() {
  const sel = loadSelections();
  // Merge selections into DATA
  const rows = DATA.map(listing => {
    const slug = listing.business_slug || '';
    const s = sel[slug] || {};
    return {
      ...listing,
      selected_hero: s.hero !== undefined ? s.hero : listing.selected_hero,
      selected_logo: s.logo !== undefined ? s.logo : listing.selected_logo,
    };
  });

  // Build CSV with all original columns plus photo_url / logo_url filled from selections
  // We only output the fields needed to UPDATE the CSV (business_slug, photo_url, logo_url)
  const lines = ['business_slug,photo_url,logo_url'];
  rows.forEach(r => {
    const slug = csvEsc(r.business_slug || '');
    const hero = csvEsc(r.selected_hero || '');
    const logo = csvEsc(r.selected_logo || '');
    lines.push(`${slug},${hero},${logo}`);
  });

  const blob = new Blob([lines.join('\\n')], { type: 'text/csv' });
  const a = document.createElement('a');
  a.href = URL.createObjectURL(blob);
  a.download = 'image_selections.csv';
  a.click();
  URL.revokeObjectURL(a.href);
}

function csvEsc(val) {
  if (val.includes(',') || val.includes('"') || val.includes('\\n')) {
    return '"' + val.replace(/"/g, '""') + '"';
  }
  return val;
}

// Boot
renderPage();
</script>
</body>
</html>
"""


def generate_curator_html(records: list[dict], html_path: Path, csv_path: str):
    data_js = json.dumps(records, indent=2, ensure_ascii=False)
    html = CURATOR_HTML.replace("__DATA_PLACEHOLDER__", data_js)
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Scrape business websites for images.")
    parser.add_argument("--file", default="baseline.csv", help="CSV file to enrich (in-place)")
    parser.add_argument("--limit", type=int, default=None, help="Max businesses to process")
    parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Skip rows that already have both photo_url and logo_url populated",
    )
    args = parser.parse_args()

    csv_path = args.file
    if not Path(csv_path).exists():
        logger.error(f"File not found: {csv_path}")
        sys.exit(1)

    run(csv_path, limit=args.limit, skip_existing=args.skip_existing)


if __name__ == "__main__":
    main()
