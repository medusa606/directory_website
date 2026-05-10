"""
Booking platform URL matcher.

Matches listings against scraped data from:
  - TheFork       → bookings/thefork.csv
  - First Table   → bookings/firsttable.csv
  - Quandoo       → bookings/quandoo.csv
  - DesignMyNight → bookings/designmynight.csv
  - ResDiary      → bookings/resdiary.csv  (already per-listing matched)

Architecture mirrors match_delivery_urls.py exactly.

Scoring strategy for booking platforms:
  - City slug exact match is REQUIRED (city data is available for all platforms)
  - Name fuzzy match carries most weight
  - Address partial match as tiebreaker (when available)
  - Business slug bonus for exact URL slug matches

Auto-update thresholds are slightly tighter than delivery (city match alone
isn't as discriminating as postcode, so we require a higher name score).

Output files (written to bookings/):
  listings_with_bookings.csv    — listings with booking URL columns filled in
  booking_matches_review.csv    — all candidate matches for human review

Usage (run from bookings/ directory):
  python match_booking_urls.py

Config:
  OVERWRITE_EXISTING = False   # set True to re-process already-matched listings
"""

import os
import re
import unicodedata
import pandas as pd
from rapidfuzz import fuzz

_HERE = os.path.dirname(os.path.abspath(__file__))


def _path(filename):
    return os.path.join(_HERE, filename)


# ============================================================
# Config
# ============================================================

LISTINGS_CSV = _path("listings.csv")
THEFORK_CSV = _path("thefork.csv")
FIRSTTABLE_CSV = _path("firsttable.csv")
QUANDOO_CSV = _path("quandoo.csv")
DMN_CSV = _path("designmynight.csv")
RESDIARY_CSV = _path("resdiary.csv")

OUTPUT_LISTINGS_CSV = _path("listings_with_bookings.csv")
OUTPUT_REVIEW_CSV = _path("booking_matches_review.csv")

OVERWRITE_EXISTING = False

# Auto-update thresholds (score out of 100)
THEFORK_AUTO_THRESHOLD = 80
FIRSTTABLE_AUTO_THRESHOLD = 80
QUANDOO_AUTO_THRESHOLD = 80
DMN_AUTO_THRESHOLD = 78
RESDIARY_AUTO_THRESHOLD = 82   # ddgs results are already highly targeted

MIN_GAP_BETWEEN_BEST_AND_SECOND = 10


# ============================================================
# Normalisation helpers (mirrors match_delivery_urls.py)
# ============================================================

def normalise_text(value):
    if pd.isna(value):
        return ""
    value = str(value).strip().lower()
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    value = re.sub(r"[^a-z0-9]+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def normalise_slug(value):
    return normalise_text(value)


def empty_value(value):
    if pd.isna(value):
        return True
    return str(value).strip() == ""


def get_best_and_second(matches):
    if not matches:
        return None, None
    matches = sorted(matches, key=lambda x: x["score"], reverse=True)
    best = matches[0]
    second = matches[1] if len(matches) > 1 else None
    return best, second


# ============================================================
# Load CSVs (graceful: skip missing files)
# ============================================================

def _load_csv(path):
    if os.path.exists(path):
        return pd.read_csv(path, dtype=str).fillna("")
    print(f"  ⚠ CSV not found, skipping: {path}")
    return pd.DataFrame()


listings = pd.read_csv(LISTINGS_CSV, dtype=str).fillna("")

unnamed_cols = [col for col in listings.columns if str(col).startswith("Unnamed")]
if unnamed_cols:
    listings = listings.drop(columns=unnamed_cols)

thefork = _load_csv(THEFORK_CSV)
firsttable = _load_csv(FIRSTTABLE_CSV)
quandoo = _load_csv(QUANDOO_CSV)
dmn = _load_csv(DMN_CSV)
resdiary = _load_csv(RESDIARY_CSV)


# ============================================================
# Ensure required listings columns exist
# ============================================================

required_listing_cols = [
    "id", "name", "address", "city_slug", "area_slug", "business_slug",
    "booking_thefork", "booking_firsttable", "booking_quandoo",
    "booking_designmynight", "booking_resdiary",
]

for col in required_listing_cols:
    if col not in listings.columns:
        listings[col] = ""


# ============================================================
# Normalise listings
# ============================================================

listings["_name_norm"] = listings["name"].apply(normalise_text)
listings["_address_norm"] = listings["address"].apply(normalise_text)
listings["_city_slug_norm"] = listings["city_slug"].apply(lambda x: str(x).strip().lower())
listings["_area_slug_norm"] = listings["area_slug"].apply(lambda x: str(x).strip().lower())
listings["_business_slug_norm"] = listings["business_slug"].apply(lambda x: str(x).strip().lower())


# ============================================================
# Normalise platform data
# All booking platform CSVs share columns: service, name, city, address, url
# ResDiary shares: service, name, city, url
# ============================================================

def _normalise_platform(df, name_col="name", city_col="city", address_col="address"):
    if df.empty:
        return df
    for col in ["service", "name", "city", "url"]:
        if col not in df.columns:
            df[col] = ""
    if address_col not in df.columns:
        df[address_col] = ""
    df["_name_norm"] = df[name_col].apply(normalise_text)
    df["_slug_norm"] = df[name_col].apply(lambda x: str(x).strip().lower())
    df["_city_slug_norm"] = df[city_col].apply(lambda x: str(x).strip().lower())
    df["_address_norm"] = df[address_col].apply(normalise_text)
    df = df[(df["url"].str.strip() != "") & (df["name"].str.strip() != "")].copy()
    return df


thefork = _normalise_platform(thefork)
firsttable = _normalise_platform(firsttable)
quandoo = _normalise_platform(quandoo)
dmn = _normalise_platform(dmn)
resdiary = _normalise_platform(resdiary)


# ============================================================
# Build lookup dictionaries: city → list of (idx, row)
# ============================================================

def _build_city_index(df):
    idx = {}
    for i, row in df.iterrows():
        city = row["_city_slug_norm"]
        if city:
            idx.setdefault(city, []).append((i, row))
    return idx


thefork_by_city = _build_city_index(thefork)
firsttable_by_city = _build_city_index(firsttable)
quandoo_by_city = _build_city_index(quandoo)
dmn_by_city = _build_city_index(dmn)
resdiary_by_city = _build_city_index(resdiary)


# ============================================================
# Scoring
# ============================================================

def score_booking_match(listing, platform_row, has_address=True):
    """
    Score a listing ↔ booking-platform row match.

    City slug must match exactly (enforced before calling this function).
    Name fuzzy match carries most of the weight.
    Address is used as a tiebreaker when available.
    """
    listing_name_norm = listing["_name_norm"]
    listing_address_norm = listing["_address_norm"]
    listing_business_slug = listing["_business_slug_norm"]

    plat_name_norm = platform_row["_name_norm"]
    plat_address_norm = platform_row["_address_norm"]
    plat_slug = platform_row["_slug_norm"]

    name_score = fuzz.token_set_ratio(listing_name_norm, plat_name_norm)
    slug_score = fuzz.token_set_ratio(listing_business_slug, plat_slug)
    best_name_score = max(name_score, slug_score)

    if has_address and plat_address_norm:
        address_score = fuzz.token_set_ratio(listing_address_norm, plat_address_norm)
        # City matched: name does heavy lifting, address is tiebreaker
        score = 25 + best_name_score * 0.60 + address_score * 0.15
    else:
        score = 25 + best_name_score * 0.75

    exact_slug_match = (
        listing_business_slug != ""
        and plat_slug != ""
        and listing_business_slug == plat_slug
    )
    if exact_slug_match:
        score += 8

    score = min(score, 100)

    return {
        "score": round(score, 2),
        "name_score": round(name_score, 2),
        "slug_score": round(slug_score, 2),
        "address_score": round(fuzz.token_set_ratio(listing_address_norm, plat_address_norm), 2)
        if has_address and plat_address_norm else "",
        "exact_slug_match": exact_slug_match,
    }


# ============================================================
# Generic matching loop
# ============================================================

review_rows = []


def _run_match(platform_name, platform_by_city, listing_col,
               auto_threshold, has_address=True):
    """
    Run the matching loop for one booking platform and append to review_rows.
    Updates listings[listing_col] for auto-updated matches.
    """
    matched = 0
    for listing_idx, listing in listings.iterrows():

        if not OVERWRITE_EXISTING and not empty_value(listing.get(listing_col, "")):
            continue

        city = listing["_city_slug_norm"]
        if not city:
            continue

        candidates = platform_by_city.get(city, [])
        if not candidates:
            continue

        candidate_matches = []
        for plat_idx, plat_row in candidates:
            scores = score_booking_match(listing, plat_row, has_address=has_address)
            if scores["score"] < 60:
                continue
            candidate_matches.append({
                "service": platform_name,
                "listing_index": listing_idx,
                "listing_id": listing["id"],
                "listing_name": listing["name"],
                "listing_address": listing["address"],
                "listing_city_slug": listing["city_slug"],
                "listing_area_slug": listing["area_slug"],
                "listing_business_slug": listing["business_slug"],
                "platform_name": plat_row["name"],
                "platform_address": plat_row.get("address", ""),
                "platform_city": plat_row["city"] if "city" in plat_row.index else "",
                "url": plat_row["url"],
                **scores,
                "second_best_score": "",
                "gap_to_second": "",
                "auto_updated": False,
                "reason": "",
            })

        best, second = get_best_and_second(candidate_matches)
        if best:
            second_score = second["score"] if second else None
            gap = best["score"] - second_score if second else 999
            best["second_best_score"] = second_score if second_score is not None else ""
            best["gap_to_second"] = round(gap, 2)

            should_update = (
                best["score"] >= auto_threshold
                and gap >= MIN_GAP_BETWEEN_BEST_AND_SECOND
            )
            if should_update:
                listings.at[listing_idx, listing_col] = best["url"]
                best["auto_updated"] = True
                best["reason"] = f"high confidence {platform_name} match"
                matched += 1
            else:
                best["reason"] = "needs review"

            review_rows.append(best)

    return matched


# ============================================================
# Run matching for each platform
# ============================================================

print("Matching TheFork…")
if not thefork.empty:
    m = _run_match("thefork", thefork_by_city, "booking_thefork",
                   THEFORK_AUTO_THRESHOLD, has_address=True)
    print(f"  → {m} auto-updated")
else:
    print("  ⚠ Skipped (no data)")

print("Matching First Table…")
if not firsttable.empty:
    m = _run_match("firsttable", firsttable_by_city, "booking_firsttable",
                   FIRSTTABLE_AUTO_THRESHOLD, has_address=True)
    print(f"  → {m} auto-updated")
else:
    print("  ⚠ Skipped (no data)")

print("Matching Quandoo…")
if not quandoo.empty:
    m = _run_match("quandoo", quandoo_by_city, "booking_quandoo",
                   QUANDOO_AUTO_THRESHOLD, has_address=True)
    print(f"  → {m} auto-updated")
else:
    print("  ⚠ Skipped (no data)")

print("Matching DesignMyNight…")
if not dmn.empty:
    m = _run_match("designmynight", dmn_by_city, "booking_designmynight",
                   DMN_AUTO_THRESHOLD, has_address=True)
    print(f"  → {m} auto-updated")
else:
    print("  ⚠ Skipped (no data)")

print("Matching ResDiary/DishCult…")
if not resdiary.empty:
    m = _run_match("resdiary", resdiary_by_city, "booking_resdiary",
                   RESDIARY_AUTO_THRESHOLD, has_address=False)
    print(f"  → {m} auto-updated")
else:
    print("  ⚠ Skipped (no data)")


# ============================================================
# Output files
# ============================================================

helper_cols = [
    "_name_norm",
    "_address_norm",
    "_city_slug_norm",
    "_area_slug_norm",
    "_business_slug_norm",
]

listings_output = listings.drop(columns=[c for c in helper_cols if c in listings.columns])
listings_output.to_csv(OUTPUT_LISTINGS_CSV, index=False)

review_df = pd.DataFrame(review_rows)

if not review_df.empty:
    review_df = review_df.sort_values(
        by=["auto_updated", "service", "score"],
        ascending=[False, True, False]
    )

review_df.to_csv(OUTPUT_REVIEW_CSV, index=False)

print()
print("Done.")
print(f"Updated listings written to: {OUTPUT_LISTINGS_CSV}")
print(f"Review file written to:      {OUTPUT_REVIEW_CSV}")

if not review_df.empty:
    print()
    print("Summary:")
    print(review_df.groupby(["service", "auto_updated"]).size())
else:
    print("No possible matches found.")
