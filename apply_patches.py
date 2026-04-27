#!/usr/bin/env python3
"""
apply_patches.py — Apply approved tag/category patches to listings CSV
======================================================================
Reads approved_patches.json (exported from tag_auditor.html) and the
source listings CSV, applies every approved change, and writes the
result to listings_rows-02a.csv.

Usage:
  python apply_patches.py
  python apply_patches.py --patches approved_patches.json \\
                          --input  db_backup/listings_rows-02.csv \\
                          --output listings_rows-02a.csv
"""

import argparse
import csv
import json
import os
import sys

DEFAULT_PATCHES = "approved_patches.json"
DEFAULT_INPUT   = os.path.join("db_backup", "listings_rows-02.csv")
DEFAULT_OUTPUT  = "listings_rows-02a.csv"


def parse_tags(tags_str: str) -> list[str]:
    if not tags_str or not tags_str.strip():
        return []
    try:
        result = json.loads(tags_str)
        return [str(t).strip() for t in result if t] if isinstance(result, list) else []
    except (json.JSONDecodeError, TypeError):
        return [t.strip().strip("[]\"'") for t in tags_str.split(",") if t.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="Apply approved tag/category patches to listings CSV"
    )
    parser.add_argument("--patches", default=DEFAULT_PATCHES,
                        help=f"Approved patches JSON (default: {DEFAULT_PATCHES})")
    parser.add_argument("--input",   default=DEFAULT_INPUT,
                        help=f"Source CSV (default: {DEFAULT_INPUT})")
    parser.add_argument("--output",  default=DEFAULT_OUTPUT,
                        help=f"Output CSV (default: {DEFAULT_OUTPUT})")
    args = parser.parse_args()

    for path in [args.patches, args.input]:
        if not os.path.exists(path):
            print(f"ERROR: File not found: {path}")
            sys.exit(1)

    with open(args.patches, encoding="utf-8") as f:
        patches_list: list[dict] = json.load(f)

    # Index patches by listing id for O(1) lookup
    patches_by_id: dict[str, dict] = {}
    for patch in patches_list:
        row_id = patch.get("id", "")
        if row_id:
            patches_by_id[row_id] = patch

    print(f"Patches loaded : {len(patches_by_id)}")

    with open(args.input, newline="", encoding="utf-8") as f:
        reader   = csv.DictReader(f)
        fieldnames = list(reader.fieldnames)  # type: ignore
        rows     = list(reader)

    # Ensure new columns exist in fieldnames
    for col in ["secondary_category", "secondary_category_slug", "image_category", "category_slug", "ranking_tier", "status", "google_rating", "google_review_count"]:
        if col not in fieldnames:
            fieldnames.append(col)

    # Counters
    listings_patched        = 0
    categories_changed      = 0
    secondary_categories_added = 0
    image_categories_added  = 0
    ranking_tier_added      = 0
    status_changed          = 0
    category_slug_added     = 0
    google_rating_added     = 0
    google_review_count_added = 0
    tags_added              = 0
    tags_removed            = 0
    instagram_added         = 0
    facebook_added          = 0
    twitter_added           = 0
    tiktok_added            = 0
    linkedin_added          = 0
    youtube_added           = 0
    description_added       = 0
    email_added             = 0
    address_added           = 0
    phone_added             = 0
    gmaps_added             = 0
    hours_added             = 0
    change_log: list[str]   = []

    for row in rows:
        row_id = row.get("id", "")
        patch  = patches_by_id.get(row_id)
        if not patch:
            continue

        proposed = patch.get("proposed", {})
        patched  = False

        # ── Category ──────────────────────────────────────────────────────
        if proposed.get("category"):
            old_cat = row.get("category", "")
            row["category"] = proposed["category"]
            if proposed.get("category_key"):
                row["category_key"]  = proposed["category_key"]
            if proposed.get("category_slug"):
                row["category_slug"] = proposed["category_slug"]
            categories_changed += 1
            patched = True
            change_log.append(
                f"  [{row.get('name')}] category: '{old_cat}' → '{proposed['category']}'"
            )

        # ── Secondary Category ────────────────────────────────────────────
        if proposed.get("secondary_category") is not None:
            old_secondary = row.get("secondary_category", "")
            new_secondary = proposed.get("secondary_category") or ""
            if new_secondary != old_secondary:
                row["secondary_category"] = new_secondary
                if proposed.get("secondary_category_slug") is not None:
                    row["secondary_category_slug"] = proposed.get("secondary_category_slug") or ""
                if new_secondary:  # Only count if setting to a value (not clearing)
                    secondary_categories_added += 1
                patched = True
                change_log.append(
                    f"  [{row.get('name')}] secondary_category: '{old_secondary}' → '{new_secondary}'"
                )

        # ── Image Category ────────────────────────────────────────────────
        if proposed.get("image_category") is not None:
            old_image_cat = row.get("image_category", "")
            new_image_cat = proposed.get("image_category") or ""
            if new_image_cat != old_image_cat:
                row["image_category"] = new_image_cat
                if new_image_cat:  # Only count if setting to a value (not clearing)
                    image_categories_added += 1
                patched = True
                change_log.append(
                    f"  [{row.get('name')}] image_category: '{old_image_cat}' → '{new_image_cat}'"
                )

        # ── Status ────────────────────────────────────────────────────────
        if proposed.get("status") is not None:
            old_status = row.get("status", "")
            new_status = proposed.get("status") or ""
            if new_status and new_status != old_status:
                row["status"] = new_status
                status_changed += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] status: '{old_status}' → '{new_status}'")

        # ── Category Slug ─────────────────────────────────────────────────
        if proposed.get("category_slug") is not None:
            old_slug = row.get("category_slug", "")
            new_slug = proposed.get("category_slug") or ""
            if new_slug and new_slug != old_slug:
                row["category_slug"] = new_slug
                category_slug_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] category_slug: '{old_slug}' → '{new_slug}'")

        # ── Ranking Tier ──────────────────────────────────────────────────
        if proposed.get("ranking_tier") is not None:
            old_tier = row.get("ranking_tier", "")
            new_tier = proposed.get("ranking_tier") or ""
            if new_tier and new_tier != old_tier:
                row["ranking_tier"] = new_tier
                ranking_tier_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] ranking_tier: '{old_tier}' → '{new_tier}'")

        # ── Google Rating ─────────────────────────────────────────────────
        if proposed.get("google_rating") is not None:
            new_rating = proposed.get("google_rating") or ""
            if new_rating and not row.get("google_rating", "").strip():
                row["google_rating"] = new_rating
                google_rating_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] google_rating: {new_rating}")

        # ── Google Review Count ───────────────────────────────────────────
        if proposed.get("google_review_count") is not None:
            new_count = proposed.get("google_review_count") or ""
            if new_count and not row.get("google_review_count", "").strip():
                row["google_review_count"] = new_count
                google_review_count_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] google_review_count: {new_count}")

        # ── Tags ──────────────────────────────────────────────────────────
        current_tags = parse_tags(row.get("tags", ""))
        current_set  = set(current_tags)
        add_list     = proposed.get("tags_add", [])
        remove_set   = set(proposed.get("tags_remove", []))

        new_tags = [t for t in current_tags if t not in remove_set]
        added: list[str] = []
        for tag in add_list:
            if tag not in current_set:
                new_tags.append(tag)
                added.append(tag)

        removed_actual = list(remove_set & current_set)

        if added or removed_actual:
            row["tags"] = json.dumps(new_tags)
            tags_added   += len(added)
            tags_removed += len(removed_actual)
            patched = True
            if added:
                change_log.append(f"  [{row.get('name')}] tags +{added}")
            if removed_actual:
                change_log.append(f"  [{row.get('name')}] tags -{removed_actual}")

        # ── Socials ───────────────────────────────────────────────────────
        for field, counter_name in [
            ("social_instagram", "instagram_added"),
            ("social_facebook",  "facebook_added"),
            ("social_twitter",   "twitter_added"),
            ("social_tiktok",    "tiktok_added"),
            ("social_linkedin",  "linkedin_added"),
            ("social_youtube",   "youtube_added"),
        ]:
            new_val = proposed.get(field, "")
            if new_val and not row.get(field, "").strip():
                row[field] = new_val
                patched = True
                change_log.append(f"  [{row.get('name')}] {field}: {new_val}")
                if field == "social_instagram": instagram_added += 1
                if field == "social_facebook":  facebook_added  += 1
                if field == "social_twitter":   twitter_added   += 1
                if field == "social_tiktok":    tiktok_added    += 1
                if field == "social_linkedin":  linkedin_added  += 1
                if field == "social_youtube":   youtube_added   += 1

        # ── Address ───────────────────────────────────────────────────────
        if proposed.get("address") is not None:
            new_addr = proposed.get("address") or ""
            if new_addr and not row.get("address", "").strip():
                row["address"] = new_addr
                address_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] address: added")

        # ── Phone ─────────────────────────────────────────────────────────
        if proposed.get("phone") is not None:
            new_phone = proposed.get("phone") or ""
            if new_phone and not row.get("phone", "").strip():
                row["phone"] = new_phone
                phone_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] phone: {new_phone}")

        # ── Google Maps URL ───────────────────────────────────────────────
        if proposed.get("gmaps_url") is not None:
            new_gmaps = proposed.get("gmaps_url") or ""
            if new_gmaps and not row.get("google_maps_url", "").strip():
                row["google_maps_url"] = new_gmaps
                gmaps_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] google_maps_url: added")

        # ── Opening Hours ─────────────────────────────────────────────────
        if proposed.get("opening_hours") is not None:
            new_hours = proposed.get("opening_hours") or ""
            if new_hours and not row.get("opening_hours", "").strip():
                row["opening_hours"] = new_hours
                hours_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] opening_hours: added")

        # ── Description ───────────────────────────────────────────────────
        if proposed.get("description") is not None:
            new_desc = proposed.get("description") or ""
            if new_desc and not row.get("description", "").strip():
                row["description"] = new_desc
                description_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] description: added")

        # ── Email ─────────────────────────────────────────────────────────
        if proposed.get("email") is not None:
            new_email = proposed.get("email") or ""
            if new_email and not row.get("email", "").strip():
                row["email"] = new_email
                email_added += 1
                patched = True
                change_log.append(f"  [{row.get('name')}] email: {new_email}")

        if patched:
            listings_patched += 1

    # Write output
    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n{'='*60}")
    print(f"PATCHES APPLIED  →  {args.output}")
    print(f"{'='*60}")
    print(f"Listings patched        : {listings_patched}")
    print(f"Categories changed      : {categories_changed}")
    print(f"Secondary categories    : {secondary_categories_added}")
    print(f"Image categories        : {image_categories_added}")
    print(f"Status changed          : {status_changed}")
    print(f"Category slugs added    : {category_slug_added}")
    print(f"Ranking tiers added     : {ranking_tier_added}")
    print(f"Google ratings added    : {google_rating_added}")
    print(f"Google review counts    : {google_review_count_added}")
    print(f"Tags added              : {tags_added}")
    print(f"Tags removed            : {tags_removed}")
    print(f"Instagram added         : {instagram_added}")
    print(f"Facebook added          : {facebook_added}")
    print(f"Twitter added           : {twitter_added}")
    print(f"TikTok added            : {tiktok_added}")
    print(f"LinkedIn added          : {linkedin_added}")
    print(f"YouTube added           : {youtube_added}")
    print(f"Descriptions added      : {description_added}")
    print(f"Emails added            : {email_added}")
    print(f"Addresses added         : {address_added}")
    print(f"Phone numbers added     : {phone_added}")
    print(f"Google Maps URLs added  : {gmaps_added}")
    print(f"Opening hours added     : {hours_added}")
    print()
    for line in change_log:
        print(line)


if __name__ == "__main__":
    main()
