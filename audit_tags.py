#!/usr/bin/env python3
"""
audit_tags.py — Meridian Directory Tag & Category Auditor
=========================================================
Reads the listings CSV and audits every record for:
  1. Missing tags implied by the business name
  2. Category mismatches (e.g. a kitchen-fitter in "Food & Produce")
  3. (optional) Website crawl to confirm/correct category and find social links

Outputs:
  tag_audit_results.json — array of per-listing audit records with proposed changes

Usage:
  python audit_tags.py                         # name analysis only, all listings
  python audit_tags.py --crawl                 # also crawl websites (slow)
  python audit_tags.py --limit 10 --crawl      # test: first 10 with crawl
  python audit_tags.py --names "Trika Yoga,Margetts & Margetts"  # specific names
  python audit_tags.py --input my.csv          # custom input file
"""

import argparse
import csv
import json
import logging
import os
import re
import sys
import time
from datetime import datetime
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Category taxonomy
# ---------------------------------------------------------------------------

CATEGORY_MAP = {
    "Art & Design":            {"key": "art_design",        "slug": "art-and-design"},
    "Cafes & Coffee":          {"key": "restaurants_cafes",  "slug": "cafes"},
    "Craft & Makers":          {"key": "craft_makers",       "slug": "craft-and-makers"},
    "Drinks & Brewing":        {"key": "drinks_brewing",     "slug": "drinks-and-brewing"},
    "Entertainment":           {"key": "entertainment",      "slug": "entertainment"},
    "Food & Produce":          {"key": "food_produce",       "slug": "food-and-produce"},
    "Health & Wellbeing":      {"key": "health_wellbeing",   "slug": "health-and-wellbeing"},
    "Home & Interiors":        {"key": "home_interiors",     "slug": "home-and-interiors"},
    "Plants & Garden":         {"key": "plants_garden",      "slug": "plants-and-garden"},
    "Restaurants & Fast Food": {"key": "restaurants_cafes",  "slug": "restaurants"},
    "Services":                {"key": "services",           "slug": "services"},
}

# ---------------------------------------------------------------------------
# Name → tag rules: (keyword_list, tag_to_add, confidence)
# Keywords are checked as substrings in the lowercased business name.
# Rules are skipped when the tag is already present.
# ---------------------------------------------------------------------------

NAME_TAG_RULES = [
    # Health & wellbeing
    (["yoga"],                              "yoga",            0.95),
    (["pilates"],                           "pilates",         0.95),
    (["barber", "barbershop", "barbers"],   "hairdresser",     0.88),
    (["spa "],                              "massage",         0.80),
    # Food types — name implies specific tag
    (["pizza", "pizzeria"],                 "pizza",           0.93),
    (["burger", "burgers"],                 "burger",          0.92),
    (["kebab", "kebabs"],                   "kebab",           0.93),
    (["sushi"],                             "sushi",           0.92),
    (["thai"],                              "thai",            0.90),
    (["chinese"],                           "chinese",         0.90),
    (["indian", "tandoor", "tandoori"],     "indian",          0.88),
    (["vietnamese", "viet "],               "vietnamese",      0.90),
    (["italian"],                           "italian",         0.85),
    (["mexican", "burrito", "taco"],        "mexican",         0.90),
    (["lebanese"],                          "lebanese",        0.90),
    (["moroccan"],                          "moroccan",        0.90),
    (["falafel"],                           "falafel",         0.90),
    (["noodle", "ramen", "pho"],            "noodle",          0.88),
    (["fish and chip", "fish & chip", "chippy", "fish bar"], "fish_and_chips", 0.88),
    (["bakery", "bakers"],                  "bakery",          0.90),
    (["deli", "delicatessen"],              "deli",            0.90),
    (["butcher", "butchers"],               "butcher",         0.90),
    (["ice cream", "gelato", "sorbet"],     "ice_cream",       0.90),
    # Drinks
    (["brewery", "brewing"],                "brewery",         0.92),
    (["taproom", "tap room"],               "bar",             0.85),
    # Retail / services
    (["florist", "flowers", "floral"],      "florist",         0.90),
    (["pharmacy", "chemist"],               "pharmacy",        0.93),
    (["dental", "dentist"],                 "dentist",         0.93),
    (["theatre", "theater"],               "theatre",          0.95),
    (["gallery"],                           "gallery",         0.88),
    (["tailor", "tailoring"],               "tailor",          0.90),
    (["garden centre", "garden center"],    "garden_centre",   0.92),
]

# ---------------------------------------------------------------------------
# Name → category hints: (keyword_list, suggested_category)
# First match wins. Only triggers when current category differs.
# ---------------------------------------------------------------------------

NAME_CATEGORY_HINTS = [
    (["yoga", "pilates"],                                              "Health & Wellbeing"),
    (["brewery", "brewing", "taproom", "tap room", "craft beer"],      "Drinks & Brewing"),
    (["theatre", "theater", "cinema"],                                 "Entertainment"),
    (["florist", "flower shop", "flowers"],                            "Plants & Garden"),
    (["garden centre", "garden center", "plant nursery"],              "Plants & Garden"),
    # Home & Interiors — be specific to avoid false positives
    (["kitchen designer", "kitchen fitter", "fitted kitchen",
      "bespoke kitchen", "handcrafted kitchen", "kitchen specialist"],  "Home & Interiors"),
    (["bespoke furniture", "furniture maker", "joinery",
      "interior designer", "interior design", "home furnishing"],       "Home & Interiors"),
    (["art gallery", "gallery"],                                        "Art & Design"),
    (["pizza", "pizzeria", "burger joint", "kebab shop",
      "fish and chip", "fish & chip", "chippy"],                        "Restaurants & Fast Food"),
    (["cafe", "café", "caffè", "coffee lounge", "espresso bar"],       "Cafes & Coffee"),
    (["farm shop", "farmshop", "farm store"],                          "Food & Produce"),
    (["butcher", "butchers"],                                          "Food & Produce"),
    (["deli", "delicatessen"],                                         "Food & Produce"),
]

# Any of these tags in the current tag list suggest the listing IS food/dining
_FOOD_TAGS = {
    "bakery", "baker", "deli", "butcher", "fishmonger", "greengrocer",
    "pizza", "burger", "kebab", "restaurant", "cafe", "fast_food",
    "convenience", "supermarket", "pub", "bar", "ice_cream", "sandwich",
    "fish_and_chips", "italian", "indian", "chinese", "thai", "vietnamese",
    "mexican", "noodle", "falafel", "lebanese", "moroccan",
}

# Any of these words in the business name suggest it IS a food business
_FOOD_NAME_WORDS = {
    "cafe", "café", "caffe", "coffee", "restaurant", "eatery", "bistro",
    "brasserie", "diner", "kitchen", "food", "pizza", "burger", "kebab",
    "fish", "chip", "bakery", "bakers", "deli", "delicatessen", "grocery",
    "farm shop", "butcher", "sushi", "curry", "tandoor", "noodle", "falafel",
    "takeaway", "grill", "bbq", "barbecue", "canteen", "dining",
    "gelato", "ice cream", "patisserie",
}

# ---------------------------------------------------------------------------
# Website crawl: category keyword sets
# Scoring: strong match = 3 points, weak match = 1 point
# ---------------------------------------------------------------------------

WEBSITE_CATEGORY_KEYWORDS = {
    "Restaurants & Fast Food": {
        "strong": [
            "view our menu", "book a table", "make a reservation", "our menu",
            "dine with us", "restaurant", "cuisine", "starter", "main course",
            "dessert", "order online", "delivery menu", "takeaway menu",
        ],
        "weak": ["food", "eat", "lunch", "dinner", "breakfast", "meal", "dish"],
    },
    "Cafes & Coffee": {
        "strong": [
            "coffee", "espresso", "latte", "cappuccino", "flat white", "americano",
            "barista", "specialty coffee", "single origin", "brunch", "cafe",
        ],
        "weak": ["tea", "cake", "pastry", "sandwich"],
    },
    "Drinks & Brewing": {
        "strong": [
            "brewery", "we brew", "our beers", "craft beer", "ale", "lager",
            "taproom", "hops", "malt", "fermentation", "keg", "cask",
        ],
        "weak": ["beer", "bar", "drink", "pint"],
    },
    "Health & Wellbeing": {
        "strong": [
            "yoga", "pilates", "therapy", "treatment", "wellness", "health clinic",
            "physiotherapy", "massage", "acupuncture", "wellbeing", "clinic",
        ],
        "weak": ["health", "care", "relax", "body", "mind"],
    },
    "Home & Interiors": {
        "strong": [
            "bespoke kitchen", "fitted kitchen", "kitchen design", "kitchen fitter",
            "cabinetry", "joinery", "handcrafted kitchen", "bedroom furniture",
            "bespoke furniture", "interior design", "bespoke joinery",
            "handcrafting", "heart of your home",
        ],
        "weak": ["kitchen", "furniture", "home", "interior", "bespoke"],
    },
    "Food & Produce": {
        "strong": [
            "farm shop", "fresh produce", "artisan food", "organic produce",
            "locally sourced", "our produce", "food producer", "butchery",
        ],
        "weak": ["fresh", "local", "seasonal", "organic"],
    },
    "Craft & Makers": {
        "strong": [
            "handmade", "craft", "maker", "workshop", "studio",
            "artisan", "hand crafted", "we make", "small batch",
        ],
        "weak": ["creative", "making", "design", "create"],
    },
    "Art & Design": {
        "strong": [
            "gallery", "exhibition", "artist", "artwork", "prints", "illustration",
            "graphic design", "fine art", "contemporary art",
        ],
        "weak": ["art", "creative", "visual"],
    },
    "Plants & Garden": {
        "strong": [
            "garden centre", "plant nursery", "florist", "floral design",
            "landscaping", "garden design", "fresh flowers",
        ],
        "weak": ["garden", "plant", "flower", "outdoor", "grow"],
    },
    "Entertainment": {
        "strong": [
            "theatre", "cinema", "live music", "events venue", "nightclub",
            "comedy club", "live performance",
        ],
        "weak": ["entertainment", "show", "performance", "event"],
    },
    "Services": {
        "strong": [
            "dry cleaning", "laundry service", "tailoring", "alterations",
            "repair service",
        ],
        "weak": ["service", "professional", "repair"],
    },
}
# Instagram category mapping to our categories
INSTAGRAM_CATEGORY_MAP = {
    "restaurant": "Restaurants & Fast Food",
    "cafe": "Cafes & Coffee",
    "coffee": "Cafes & Coffee",
    "bakery": "Food & Produce",
    "bar": "Drinks & Brewing",
    "brewery": "Drinks & Brewing",
    "yoga": "Health & Wellbeing",
    "fitness": "Fitness & Sports",
    "gym": "Fitness & Sports",
    "spa": "Health & Wellbeing",
    "salon": "Services",
    "barber": "Services",
    "gallery": "Art & Design",
    "art": "Art & Design",
    "florist": "Plants & Garden",
    "flower": "Plants & Garden",
    "shop": "Services",
    "store": "Services",
    "boutique": "Services",
    "furniture": "Home & Interiors",
    "design": "Home & Interiors",
    "craft": "Craft & Makers",
    "maker": "Craft & Makers",
    "artist": "Art & Design",
    "entertainment": "Entertainment",
    "theater": "Entertainment",
    "theatre": "Entertainment",
}
# Social link patterns used during website crawl
_SOCIAL_PATTERNS = {
    "social_instagram": (
        r"https?://(?:www\.)?instagram\.com/"
        r"(?!explore|accounts|p/|reel/|reels/|stories/|direct|about|developer|legal)"
        r"([a-zA-Z0-9._]+)"
    ),
    "social_facebook": (
        r"https?://(?:www\.)?(?:en-gb\.)?facebook\.com/"
        r"(?!sharer|share|tr|flx|plugins|login|recover|help|policies|"
        r"hashtag|watch|marketplace|gaming|events|pages/create|ads|business|dialog|"
        r"2008|fbml|v\d)"
        r"([a-zA-Z0-9._/-]+)"
    ),
    "social_twitter": (
        r"https?://(?:www\.)?(?:twitter\.com|x\.com)/"
        r"(?!intent|share|search|i/|hashtag|home|explore|settings|tos|privacy)"
        r"([a-zA-Z0-9._]+)"
    ),
    "social_tiktok": (
        r"https?://(?:www\.)?tiktok\.com/"
        r"(?!discover|explore|foryou|trending|share)"
        r"@?([a-zA-Z0-9._-]+)"
    ),
    "social_linkedin": (
        r"https?://(?:www\.)?linkedin\.com/"
        r"(?:company|in)/"
        r"([a-zA-Z0-9_-]+)"
    ),
    "social_youtube": (
        r"https?://(?:www\.)?(?:youtube\.com|youtu\.be)/"
        r"(?:c|user|channel|watch\?v=)"
        r"([a-zA-Z0-9_-]+)"
    ),
}

_HTTP_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def parse_tags(tags_str: str) -> list[str]:
    """Parse JSON tag array string → list. Tolerates malformed input."""
    if not tags_str or not tags_str.strip():
        return []
    try:
        result = json.loads(tags_str)
        if isinstance(result, list):
            return [str(t).strip() for t in result if t]
        return []
    except (json.JSONDecodeError, TypeError):
        return [t.strip().strip("[]\"'") for t in tags_str.split(",") if t.strip()]


def _fetch(url: str, timeout: int = 10) -> str:
    """Fetch URL, return text or empty string on failure."""
    try:
        resp = requests.get(url, timeout=timeout, headers=_HTTP_HEADERS, allow_redirects=True)
        if resp.status_code == 200:
            return resp.text
    except Exception:
        pass
    return ""


# ---------------------------------------------------------------------------
# Phase 1: Name analysis
# ---------------------------------------------------------------------------

def analyse_name(row: dict) -> dict:
    """
    Analyse business name/tags for missing tags and category mismatches.
    Returns proposed changes dict.
    """
    name = row.get("name", "")
    name_lower = name.lower()
    current_category = row.get("category", "")
    current_tags = parse_tags(row.get("tags", ""))
    current_tags_set = set(current_tags)

    tags_to_add: list[str] = []
    reasons: list[str] = []
    suggested_category: str | None = None
    confidence = 0.0

    # --- Tag rules ---
    for keywords, tag, conf in NAME_TAG_RULES:
        if tag in current_tags_set:
            continue
        for kw in keywords:
            if kw.strip() in name_lower:
                tags_to_add.append(tag)
                reasons.append(f"name contains '{kw.strip()}' → add tag '{tag}'")
                confidence = max(confidence, conf)
                break

    # --- Category hints ---
    for keywords, hint_cat in NAME_CATEGORY_HINTS:
        for kw in keywords:
            if kw.lower() in name_lower:
                if hint_cat != current_category:
                    suggested_category = hint_cat
                    confidence = max(confidence, 0.85)
                    reasons.append(
                        f"name contains '{kw}' → suggests category "
                        f"'{hint_cat}' (currently '{current_category}')"
                    )
                break
        if suggested_category:
            break

    # --- Food & Produce conflict check ---
    # Flag listings in Food & Produce that have no food signals at all
    if current_category == "Food & Produce" and not suggested_category:
        name_has_food = any(kw in name_lower for kw in _FOOD_NAME_WORDS)
        tags_have_food = bool(current_tags_set & _FOOD_TAGS)
        if not name_has_food and not tags_have_food:
            reasons.append(
                f"flagged: category 'Food & Produce' but name and tags have no "
                f"food indicators (tags: {current_tags}) — website check recommended"
            )
            confidence = max(confidence, 0.55)

    # Remove duplicates, preserve order
    seen: set[str] = set()
    deduped_tags = []
    for t in tags_to_add:
        if t not in seen:
            seen.add(t)
            deduped_tags.append(t)

    return {
        "tags_add": deduped_tags,
        "tags_remove": [],
        "suggested_category": suggested_category,
        "confidence": round(confidence, 2),
        "reasons": reasons,
        "source": "name_analysis",
    }


# ---------------------------------------------------------------------------
# Phase 2: Website crawl
# ---------------------------------------------------------------------------

def _classify_content(text: str) -> tuple[str, float]:
    """Score page text against category keywords. Returns (category, confidence)."""
    if not text:
        return ("", 0.0)

    text_lower = text.lower()
    scores: dict[str, float] = {}

    for cat, kws in WEBSITE_CATEGORY_KEYWORDS.items():
        score = 0.0
        for kw in kws.get("strong", []):
            if kw.lower() in text_lower:
                score += 3.0
        for kw in kws.get("weak", []):
            if kw.lower() in text_lower:
                score += 1.0
        scores[cat] = score

    sorted_scores = sorted(scores.items(), key=lambda x: -x[1])
    best_cat, best_score = sorted_scores[0]
    second_score = sorted_scores[1][1] if len(sorted_scores) > 1 else 0.0

    if best_score < 3.0:  # require at least one strong match
        return ("", 0.0)

    margin = best_score - second_score
    confidence = min(0.5 + (margin / (best_score + 1.0)) * 0.5, 0.95)
    return (best_cat, round(confidence, 2))


def _extract_socials(html: str, existing: dict) -> dict[str, str]:
    """Find social URLs in raw HTML that aren't already in existing."""
    found = {}
    for field, pattern in _SOCIAL_PATTERNS.items():
        if existing.get(field, "").strip():
            continue  # already have it
        match = re.search(pattern, html, re.IGNORECASE)
        if match:
            url = match.group(0)
            path = urlparse(url).path.strip("/")
            if path and len(path) > 1:
                found[field] = url
    return found


def _extract_contact_info(html: str, existing: dict) -> dict[str, str]:
    """Extract email and phone from raw HTML if not already in existing."""
    found = {}
    
    # Extract email if not already present
    if not existing.get("email", "").strip():
        # Look for mailto: links and common email patterns
        email_patterns = [
            r'mailto:([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
            r'([a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})',
        ]
        for pattern in email_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                email = match.group(1).strip()
                if email and len(email) < 120:  # sanity check
                    found["email"] = email
                    break
    
    # Extract phone if not already present
    if not existing.get("phone", "").strip():
        # Look for common UK phone patterns
        phone_patterns = [
            r'tel:(\+?44[0-9\s\-\(\)]{10,})',  # tel: links with UK numbers
            r'(\+?44[0-9\s\-\(\)]{10,})',      # International format
            r'(0[0-9]{1,3}[\s\-\(]?[0-9]{2,}[\s\-\)]?[0-9]{2,}[\s\-]?[0-9]{2,})',  # Local format
        ]
        for pattern in phone_patterns:
            match = re.search(pattern, html, re.IGNORECASE)
            if match:
                phone = match.group(1).strip()
                if phone and len(phone) < 30:  # sanity check
                    found["phone"] = phone
                    break
    
    return found


def _extract_instagram_category(html: str) -> str | None:
    """Extract category from Instagram profile page HTML.
    Looks for pattern: <div dir="auto">Restaurant</div>"""
    match = re.search(r'<div dir="auto">([^<]+)</div>', html)
    if match:
        return match.group(1).strip()
    return None


def _instagram_category_to_meridian(ig_category: str) -> str | None:
    """Map Instagram category to Meridian category."""
    if not ig_category:
        return None
    ig_lower = ig_category.lower()
    return INSTAGRAM_CATEGORY_MAP.get(ig_lower)


def crawl_instagram_profile(username: str) -> dict:
    """Fetch Instagram profile page and extract category."""
    result = {
        "ig_category": None,
        "ig_confidence": 0.75,
        "ig_reasons": [],
        "ig_crawled": False,
    }

    if not username:
        return result

    profile_url = f"https://www.instagram.com/{username}/"
    html = _fetch(profile_url, timeout=10)
    if not html:
        return result
    result["ig_crawled"] = True

    ig_category = _extract_instagram_category(html)
    if ig_category:
        meridian_category = _instagram_category_to_meridian(ig_category)
        if meridian_category:
            result["ig_category"] = meridian_category
            result["ig_reasons"].append(
                f"Instagram profile category: '{ig_category}' → '{meridian_category}'"
            )

    return result


def crawl_website(url: str, current_category: str, existing_socials: dict) -> dict:
    """Crawl a website; return category suggestion and any discovered social links."""
    result = {
        "crawl_category": None,
        "crawl_confidence": 0.0,
        "socials": {},
        "contact": {},
        "crawl_reasons": [],
        "crawled": False,
    }

    if not url:
        return result

    # Fetch homepage
    html = _fetch(url)
    if not html:
        return result
    result["crawled"] = True

    # Fetch about page for more signal
    base = url.rstrip("/")
    for sub in ["/about", "/about-us"]:
        extra = _fetch(f"{base}{sub}", timeout=7)
        if extra:
            html += extra

    # Classify
    crawl_cat, crawl_conf = _classify_content(html)
    result["crawl_category"] = crawl_cat
    result["crawl_confidence"] = crawl_conf

    if crawl_cat and crawl_cat != current_category and crawl_conf >= 0.65:
        result["crawl_reasons"].append(
            f"website suggests '{crawl_cat}' (confidence {crawl_conf:.0%})"
        )

    # Social links
    socials = _extract_socials(html, existing_socials)
    result["socials"] = socials
    for field, link in socials.items():
        result["crawl_reasons"].append(f"found {field}: {link}")

    # Contact info (email, phone)
    existing_contact = {
        "email": existing_socials.get("email", ""),
        "phone": existing_socials.get("phone", ""),
    }
    contact = _extract_contact_info(html, existing_contact)
    result["contact"] = contact
    for field, value in contact.items():
        result["crawl_reasons"].append(f"found {field}: {value}")

    # If we found Instagram, crawl the profile for category info
    if "social_instagram" in socials:
        ig_match = re.search(
            r"instagram\.com/([a-zA-Z0-9._]+)",
            socials["social_instagram"],
            re.IGNORECASE
        )
        if ig_match:
            ig_username = ig_match.group(1)
            ig_result = crawl_instagram_profile(ig_username)
            if ig_result["ig_category"]:
                # If website didn't suggest a category, use Instagram's
                if not result["crawl_category"]:
                    result["crawl_category"] = ig_result["ig_category"]
                    result["crawl_confidence"] = ig_result["ig_confidence"]
                result["crawl_reasons"].extend(ig_result["ig_reasons"])

    return result


# ---------------------------------------------------------------------------
# Full listing audit
# ---------------------------------------------------------------------------

def audit_listing(row: dict, do_crawl: bool) -> dict:
    """Run full audit for one listing. Returns the result record."""
    current_tags = parse_tags(row.get("tags", ""))
    existing_socials = {
        "social_instagram": row.get("social_instagram", ""),
        "social_facebook":  row.get("social_facebook",  ""),
        "social_twitter":   row.get("social_twitter",   ""),
        "social_tiktok":    row.get("social_tiktok",    ""),
        "social_linkedin":  row.get("social_linkedin",  ""),
        "social_youtube":   row.get("social_youtube",   ""),
    }

    # Phase 1: name
    name_result = analyse_name(row)
    tags_add = list(name_result["tags_add"])
    tags_remove: list[str] = list(name_result["tags_remove"])
    reasons = list(name_result["reasons"])
    suggested_category = name_result["suggested_category"]
    confidence = name_result["confidence"]
    source = "name_analysis"

    # Phase 2: website crawl (optional)
    crawl_result = {}
    if do_crawl and row.get("website", "").strip():
        crawl_result = crawl_website(
            row["website"].strip(), row.get("category", ""), existing_socials
        )
        reasons.extend(crawl_result.get("crawl_reasons", []))

        crawl_cat = crawl_result.get("crawl_category", "")
        crawl_conf = crawl_result.get("crawl_confidence", 0.0)

        if crawl_cat and crawl_cat != row.get("category", ""):
            if not suggested_category:
                # Crawl found a conflict that name didn't catch
                suggested_category = crawl_cat
                confidence = max(confidence, crawl_conf)
                source = "website_crawl"
            elif suggested_category == crawl_cat:
                # Name and crawl agree → boost confidence
                confidence = min(0.98, confidence + crawl_conf * 0.25)
                source = "name_analysis+website_crawl"
            elif crawl_conf > confidence:
                # Crawl is more confident than name → prefer it
                suggested_category = crawl_cat
                confidence = crawl_conf
                source = "website_crawl"

    # Resolve proposed category to full record
    proposed_category = None
    proposed_category_key = None
    proposed_category_slug = None
    if suggested_category and suggested_category != row.get("category", ""):
        proposed_category = suggested_category
        cat_meta = CATEGORY_MAP.get(suggested_category, {})
        proposed_category_key = cat_meta.get("key")
        proposed_category_slug = cat_meta.get("slug")

    # Post-process: if reclassifying to Home & Interiors and "kitchen" tag is present,
    # suggest replacing "kitchen" (ambiguous) with "kitchen_designer"
    current_tags_set = set(current_tags)
    if proposed_category == "Home & Interiors":
        if "kitchen" in current_tags_set and "kitchen_designer" not in current_tags_set:
            tags_add.append("kitchen_designer")
            tags_remove.append("kitchen")
            reasons.append("replacing ambiguous 'kitchen' tag with 'kitchen_designer'")

    # Proposed socials from crawl
    crawl_socials = crawl_result.get("socials", {})
    proposed_instagram = crawl_socials.get("social_instagram")
    proposed_facebook  = crawl_socials.get("social_facebook")
    proposed_twitter   = crawl_socials.get("social_twitter")
    proposed_tiktok    = crawl_socials.get("social_tiktok")
    proposed_linkedin  = crawl_socials.get("social_linkedin")
    proposed_youtube   = crawl_socials.get("social_youtube")

    # Proposed contact info from crawl
    crawl_contact = crawl_result.get("contact", {})
    proposed_email = crawl_contact.get("email")
    proposed_phone = crawl_contact.get("phone")

    # Deduplicate tags_add
    seen_add: set[str] = set()
    deduped_add = []
    for t in tags_add:
        if t not in seen_add and t not in current_tags_set:
            seen_add.add(t)
            deduped_add.append(t)

    has_changes = bool(
        deduped_add or tags_remove or proposed_category
        or proposed_instagram or proposed_facebook or proposed_twitter
        or proposed_tiktok or proposed_linkedin or proposed_youtube
        or proposed_email or proposed_phone
    )

    return {
        "id":            row.get("id", ""),
        "business_slug": row.get("business_slug", ""),
        "name":          row.get("name", ""),
        "address":       row.get("address", ""),
        "area_slug":     row.get("area_slug", ""),
        "city_slug":     row.get("city_slug", ""),
        "website":       row.get("website", ""),
        "status":        row.get("status", ""),
        "chain_flag":    row.get("chain_flag", ""),
        "current": {
            "category":      row.get("category", ""),
            "category_key":  row.get("category_key", ""),
            "category_slug": row.get("category_slug", ""),
            "tags":          current_tags,
            "description":   row.get("description", ""),
            "email":         row.get("email", ""),
            "address":       row.get("address", ""),
            "phone":         row.get("phone", ""),
            "gmaps_url":     row.get("google_maps_url", ""),
            "opening_hours": row.get("opening_hours", ""),
            "social_instagram": existing_socials["social_instagram"],
            "social_facebook":  existing_socials["social_facebook"],
            "social_twitter":   existing_socials["social_twitter"],
            "social_tiktok":    existing_socials["social_tiktok"],
            "social_linkedin":  existing_socials["social_linkedin"],
            "social_youtube":   existing_socials["social_youtube"],
        },
        "proposed": {
            "category":      proposed_category,
            "category_key":  proposed_category_key,
            "category_slug": proposed_category_slug,
            "tags_add":      deduped_add,
            "tags_remove":   tags_remove,
            "description":   None,
            "email":         proposed_email,
            "phone":         proposed_phone,
            "social_instagram": proposed_instagram,
            "social_facebook":  proposed_facebook,
            "social_twitter":   proposed_twitter,
            "social_tiktok":    proposed_tiktok,
            "social_linkedin":  proposed_linkedin,
            "social_youtube":   proposed_youtube,
        },
        "has_changes": has_changes,
        "confidence":  round(confidence, 2),
        "reasons":     reasons,
        "source":      source if reasons else "no_changes",
        "crawled":     crawl_result.get("crawled", False),
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

DEFAULT_INPUT  = os.path.join("db_backup", "listings_rows-04.csv")
DEFAULT_OUTPUT = "tag_audit_results.json"


def main():
    parser = argparse.ArgumentParser(
        description="Audit listings CSV for tag and category accuracy"
    )
    parser.add_argument("--input",  default=DEFAULT_INPUT,
                        help=f"Input CSV (default: {DEFAULT_INPUT})")
    parser.add_argument("--output", default=DEFAULT_OUTPUT,
                        help="Output JSON (default: tag_audit_results.json)")
    parser.add_argument("--crawl",  action="store_true",
                        help="Enable website crawl for deeper analysis")
    parser.add_argument("--delay",  type=float, default=1.5,
                        help="Seconds between crawls (default: 1.5)")
    parser.add_argument("--limit",  type=int, default=None,
                        help="Only process first N listings (for testing)")
    parser.add_argument("--names",  default=None,
                        help='Pipe-separated business names to target, e.g. '
                             '"Trika Yoga|Margetts & Margetts|Wiper and True Taproom, Old Market"')
    parser.add_argument("--include-chains", action="store_true",
                        help="Include chain businesses (skipped by default)")

    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"ERROR: File not found: {args.input}")
        sys.exit(1)

    with open(args.input, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))

    total = len(rows)

    # Filter by name list if provided
    target_names: set[str] | None = None
    if args.names:
        target_names = {n.strip().lower() for n in args.names.split("|") if n.strip()}

    # Build the list to process
    rows_to_process = rows[:args.limit] if args.limit else rows

    # Apply name filter (after limit so --limit N still caps iterations)
    if target_names:
        rows_to_process = [
            r for r in rows_to_process
            if r.get("name", "").lower() in target_names
        ]  # Use | as delimiter in --names to handle business names containing commas

    log.info(f"Auditing {len(rows_to_process)} of {total} listings")
    if args.crawl:
        log.info(f"Website crawl ENABLED (delay: {args.delay}s)")
    else:
        log.info("Website crawl DISABLED — use --crawl to enable")

    results = []
    skipped_chains = 0
    has_changes_count = 0

    for idx, row in enumerate(rows_to_process):
        name = row.get("name", "Unknown")
        is_chain = row.get("chain_flag", "").lower() == "true"

        if is_chain and not args.include_chains:
            skipped_chains += 1
            continue

        log.info(f"[{idx+1}/{len(rows_to_process)}] {name}")

        result = audit_listing(row, do_crawl=args.crawl)
        results.append(result)

        if result["has_changes"]:
            has_changes_count += 1
            log.info(
                f"  → changes: tags+{result['proposed']['tags_add']} "
                f"cat={result['proposed']['category'] or '—'} "
                f"confidence={result['confidence']:.0%}"
            )

        # Polite delay between crawls
        if args.crawl and row.get("website", "").strip():
            time.sleep(args.delay)

    # Write output
    output_data = {
        "generated_at":    datetime.now().isoformat(),
        "input_file":      args.input,
        "total_in_csv":    total,
        "processed":       len(results),
        "skipped_chains":  skipped_chains,
        "has_changes":     has_changes_count,
        "crawl_enabled":   args.crawl,
        "listings":        results,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}")
    print("AUDIT COMPLETE")
    print(f"{'='*60}")
    print(f"Listings processed : {len(results)}")
    print(f"Chains skipped     : {skipped_chains}")
    print(f"Have proposed changes: {has_changes_count}")
    print(f"Output             : {args.output}")
    print()


if __name__ == "__main__":
    main()
