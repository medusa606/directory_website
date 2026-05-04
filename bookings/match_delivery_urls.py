import re
import unicodedata
import pandas as pd
from rapidfuzz import fuzz


# ============================================================
# Config
# ============================================================

LISTINGS_CSV = "listings.csv"
UBER_CSV = "uber-eats.csv"
DELIVEROO_CSV = "deliveroo.csv"

OUTPUT_LISTINGS_CSV = "listings.updated.csv"
OUTPUT_REVIEW_CSV = "delivery_matches_review.csv"

# If False, existing deliveroo_url / uber_eats_url values will not be replaced
OVERWRITE_EXISTING = False

# Auto-update thresholds
UBER_AUTO_THRESHOLD = 82
DELIVEROO_AUTO_THRESHOLD = 80

# If the best match is only slightly better than the second-best match,
# skip auto-update and send it to review.
MIN_GAP_BETWEEN_BEST_AND_SECOND = 8


# ============================================================
# Normalisation helpers
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
    """
    Converts:
      ashley-down-and-bishopston
    to:
      ashley down and bishopston
    """
    return normalise_text(value)


def normalise_postcode(value):
    if pd.isna(value):
        return ""

    return re.sub(r"\s+", "", str(value).upper().strip())


def extract_uk_postcode(value):
    """
    Extracts a UK postcode from address text.

    Example:
      "397 Gloucester Road, Bristol, BS7 8TS"
    returns:
      "BS78TS"
    """
    if pd.isna(value):
        return ""

    text = str(value).upper()

    pattern = r"\b([A-Z]{1,2}[0-9][0-9A-Z]?\s*[0-9][A-Z]{2})\b"
    match = re.search(pattern, text)

    if not match:
        return ""

    return normalise_postcode(match.group(1))


def empty_value(value):
    if pd.isna(value):
        return True

    return str(value).strip() == ""


def slug_contains_area(delivery_area_slug, listing_area_slug):
    """
    Checks whether a listings area_slug exists inside a delivery area.

    Example:
      listing_area_slug = ashley-down
      delivery_area_slug = ashley-down-and-bishopston
      returns True

      listing_area_slug = easton
      delivery_area_slug = st-judes-and-easton
      returns True
    """
    if not delivery_area_slug or not listing_area_slug:
        return False

    delivery_area_slug = str(delivery_area_slug).strip().lower()
    listing_area_slug = str(listing_area_slug).strip().lower()

    if delivery_area_slug == listing_area_slug:
        return True

    # Direct slug containment catches:
    # ashley-down in ashley-down-and-bishopston
    # easton in st-judes-and-easton
    pattern = rf"(^|-){re.escape(listing_area_slug)}($|-)"
    return re.search(pattern, delivery_area_slug) is not None


def get_best_and_second(matches):
    if not matches:
        return None, None

    matches = sorted(matches, key=lambda x: x["score"], reverse=True)

    best = matches[0]
    second = matches[1] if len(matches) > 1 else None

    return best, second


# ============================================================
# Load CSVs
# ============================================================

listings = pd.read_csv(LISTINGS_CSV, dtype=str).fillna("")
uber = pd.read_csv(UBER_CSV, dtype=str).fillna("")
deliveroo = pd.read_csv(DELIVEROO_CSV, dtype=str).fillna("")


# Your listings CSV example has a trailing comma, which may create
# a blank column called "Unnamed: ..."
unnamed_cols = [col for col in listings.columns if str(col).startswith("Unnamed")]
if unnamed_cols:
    listings = listings.drop(columns=unnamed_cols)


# ============================================================
# Ensure required listings columns exist
# ============================================================

required_listing_cols = [
    "id",
    "name",
    "address",
    "city_slug",
    "area_slug",
    "business_slug",
    "deliveroo_url",
    "uber_eats_url",
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
listings["_postcode_norm"] = listings["address"].apply(extract_uk_postcode)


# ============================================================
# Normalise Uber Eats data
# Expected Uber columns:
# service,name,url,address,categories
# ============================================================

for col in ["service", "name", "url", "address", "categories"]:
    if col not in uber.columns:
        uber[col] = ""

uber["_name_norm"] = uber["name"].apply(normalise_text)
uber["_slug_norm"] = uber["name"].apply(lambda x: str(x).strip().lower())
uber["_address_norm"] = uber["address"].apply(normalise_text)
uber["_postcode_norm"] = uber["address"].apply(extract_uk_postcode)

# Remove unusable Uber rows
uber = uber[
    (uber["url"].str.strip() != "")
    & (uber["name"].str.strip() != "")
    & (uber["address"].str.strip() != "")
    & (uber["address"].str.lower().str.strip() != "closed")
].copy()


# ============================================================
# Normalise Deliveroo data
# Expected Deliveroo columns:
# service,name,city,area,address,url
# ============================================================

for col in ["service", "name", "city", "area", "address", "url"]:
    if col not in deliveroo.columns:
        deliveroo[col] = ""

deliveroo["_name_norm"] = deliveroo["name"].apply(normalise_text)
deliveroo["_slug_norm"] = deliveroo["name"].apply(lambda x: str(x).strip().lower())
deliveroo["_city_slug_norm"] = deliveroo["city"].apply(lambda x: str(x).strip().lower())
deliveroo["_area_slug_norm"] = deliveroo["area"].apply(lambda x: str(x).strip().lower())

deliveroo = deliveroo[
    (deliveroo["url"].str.strip() != "")
    & (deliveroo["name"].str.strip() != "")
    & (deliveroo["city"].str.strip() != "")
    & (deliveroo["area"].str.strip() != "")
].copy()


# ============================================================
# Build lookup dictionaries for speed
# ============================================================

uber_by_postcode = {}

for idx, row in uber.iterrows():
    postcode = row["_postcode_norm"]

    if postcode:
        uber_by_postcode.setdefault(postcode, []).append((idx, row))


deliveroo_by_city = {}

for idx, row in deliveroo.iterrows():
    city = row["_city_slug_norm"]

    if city:
        deliveroo_by_city.setdefault(city, []).append((idx, row))


# ============================================================
# Scoring functions
# ============================================================

def score_uber_match(listing, uber_row):
    """
    Uber has address, so use:
      - postcode match
      - business slug/name match
      - address match
    """

    listing_name_norm = listing["_name_norm"]
    listing_address_norm = listing["_address_norm"]
    listing_postcode = listing["_postcode_norm"]
    listing_business_slug = listing["_business_slug_norm"]

    uber_name_norm = uber_row["_name_norm"]
    uber_address_norm = uber_row["_address_norm"]
    uber_postcode = uber_row["_postcode_norm"]
    uber_slug = uber_row["_slug_norm"]

    name_score = fuzz.token_set_ratio(listing_name_norm, uber_name_norm)
    slug_score = fuzz.token_set_ratio(listing_business_slug, uber_slug)
    address_score = fuzz.token_set_ratio(listing_address_norm, uber_address_norm)

    best_name_score = max(name_score, slug_score)

    postcode_match = (
        listing_postcode != ""
        and uber_postcode != ""
        and listing_postcode == uber_postcode
    )

    exact_slug_match = (
        listing_business_slug != ""
        and uber_slug != ""
        and listing_business_slug == uber_slug
    )

    if postcode_match:
        score = 45 + best_name_score * 0.40 + address_score * 0.15
    else:
        score = best_name_score * 0.55 + address_score * 0.45

    if exact_slug_match:
        score += 8

    score = min(score, 100)

    return {
        "score": round(score, 2),
        "name_score": round(name_score, 2),
        "slug_score": round(slug_score, 2),
        "address_score": round(address_score, 2),
        "postcode_match": postcode_match,
        "exact_slug_match": exact_slug_match,
    }


def score_deliveroo_match(listing, deliveroo_row):
    """
    Deliveroo has no useful full address, so use:
      - city_slug exact match
      - area_slug containment
      - business slug/name fuzzy match
    """

    listing_city_slug = listing["_city_slug_norm"]
    listing_area_slug = listing["_area_slug_norm"]
    listing_business_slug = listing["_business_slug_norm"]
    listing_name_norm = listing["_name_norm"]

    deliveroo_city_slug = deliveroo_row["_city_slug_norm"]
    deliveroo_area_slug = deliveroo_row["_area_slug_norm"]
    deliveroo_slug = deliveroo_row["_slug_norm"]
    deliveroo_name_norm = deliveroo_row["_name_norm"]

    if not listing_city_slug or listing_city_slug != deliveroo_city_slug:
        return None

    area_match = slug_contains_area(deliveroo_area_slug, listing_area_slug)

    if not area_match:
        return None

    name_score = fuzz.token_set_ratio(listing_name_norm, deliveroo_name_norm)
    slug_score = fuzz.token_set_ratio(listing_business_slug, deliveroo_slug)

    best_name_score = max(name_score, slug_score)

    exact_slug_match = (
        listing_business_slug != ""
        and deliveroo_slug != ""
        and listing_business_slug == deliveroo_slug
    )

    # Area matched, so name/slug does most of the work.
    score = 35 + best_name_score * 0.65

    if exact_slug_match:
        score += 8

    score = min(score, 100)

    return {
        "score": round(score, 2),
        "name_score": round(name_score, 2),
        "slug_score": round(slug_score, 2),
        "address_score": "",
        "postcode_match": "",
        "area_match": area_match,
        "exact_slug_match": exact_slug_match,
    }


# ============================================================
# Run matching
# ============================================================

review_rows = []


# ------------------------------------------------------------
# Match Uber Eats
# ------------------------------------------------------------

for listing_idx, listing in listings.iterrows():

    if not OVERWRITE_EXISTING and not empty_value(listing.get("uber_eats_url", "")):
        continue

    candidate_matches = []

    listing_postcode = listing["_postcode_norm"]

    # Prefer Uber rows with the same postcode.
    # If no postcode candidates exist, scan all Uber rows.
    if listing_postcode and listing_postcode in uber_by_postcode:
        candidates = uber_by_postcode[listing_postcode]
    else:
        candidates = list(uber.iterrows())

    for uber_idx, uber_row in candidates:
        scores = score_uber_match(listing, uber_row)

        # Basic filter to avoid keeping obvious rubbish
        if scores["score"] < 60:
            continue

        candidate_matches.append({
            "service": "uber_eats",
            "listing_index": listing_idx,
            "listing_id": listing["id"],
            "listing_name": listing["name"],
            "listing_address": listing["address"],
            "listing_city_slug": listing["city_slug"],
            "listing_area_slug": listing["area_slug"],
            "listing_business_slug": listing["business_slug"],
            "delivery_name": uber_row["name"],
            "delivery_address": uber_row["address"],
            "delivery_city": "",
            "delivery_area": "",
            "url": uber_row["url"],
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
            best["score"] >= UBER_AUTO_THRESHOLD
            and gap >= MIN_GAP_BETWEEN_BEST_AND_SECOND
        )

        if should_update:
            listings.at[listing_idx, "uber_eats_url"] = best["url"]
            best["auto_updated"] = True
            best["reason"] = "high confidence uber eats match"
        else:
            best["reason"] = "needs review"

        review_rows.append(best)


# ------------------------------------------------------------
# Match Deliveroo
# ------------------------------------------------------------

for listing_idx, listing in listings.iterrows():

    if not OVERWRITE_EXISTING and not empty_value(listing.get("deliveroo_url", "")):
        continue

    listing_city_slug = listing["_city_slug_norm"]

    if not listing_city_slug:
        continue

    candidates = deliveroo_by_city.get(listing_city_slug, [])

    candidate_matches = []

    for deliveroo_idx, deliveroo_row in candidates:
        scores = score_deliveroo_match(listing, deliveroo_row)

        if scores is None:
            continue

        if scores["score"] < 60:
            continue

        candidate_matches.append({
            "service": "deliveroo",
            "listing_index": listing_idx,
            "listing_id": listing["id"],
            "listing_name": listing["name"],
            "listing_address": listing["address"],
            "listing_city_slug": listing["city_slug"],
            "listing_area_slug": listing["area_slug"],
            "listing_business_slug": listing["business_slug"],
            "delivery_name": deliveroo_row["name"],
            "delivery_address": deliveroo_row.get("address", ""),
            "delivery_city": deliveroo_row["city"],
            "delivery_area": deliveroo_row["area"],
            "url": deliveroo_row["url"],
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
            best["score"] >= DELIVEROO_AUTO_THRESHOLD
            and gap >= MIN_GAP_BETWEEN_BEST_AND_SECOND
        )

        if should_update:
            listings.at[listing_idx, "deliveroo_url"] = best["url"]
            best["auto_updated"] = True
            best["reason"] = "high confidence deliveroo match"
        else:
            best["reason"] = "needs review"

        review_rows.append(best)


# ============================================================
# Output files
# ============================================================

helper_cols = [
    "_name_norm",
    "_address_norm",
    "_city_slug_norm",
    "_area_slug_norm",
    "_business_slug_norm",
    "_postcode_norm",
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

print("Done.")
print(f"Updated listings written to: {OUTPUT_LISTINGS_CSV}")
print(f"Review file written to: {OUTPUT_REVIEW_CSV}")

if not review_df.empty:
    print()
    print("Summary:")
    print(review_df.groupby(["service", "auto_updated"]).size())
else:
    print("No possible matches found.")