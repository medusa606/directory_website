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

    # Counters
    listings_patched   = 0
    categories_changed = 0
    tags_added         = 0
    tags_removed       = 0
    instagram_added    = 0
    facebook_added     = 0
    twitter_added      = 0
    change_log: list[str] = []

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
        ]:
            new_val = proposed.get(field, "")
            if new_val and not row.get(field, "").strip():
                row[field] = new_val
                patched = True
                change_log.append(f"  [{row.get('name')}] {field}: {new_val}")
                if field == "social_instagram": instagram_added += 1
                if field == "social_facebook":  facebook_added  += 1
                if field == "social_twitter":   twitter_added   += 1

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
    print(f"Listings patched   : {listings_patched}")
    print(f"Categories changed : {categories_changed}")
    print(f"Tags added         : {tags_added}")
    print(f"Tags removed       : {tags_removed}")
    print(f"Instagram added    : {instagram_added}")
    print(f"Facebook added     : {facebook_added}")
    print(f"Twitter added      : {twitter_added}")
    print()
    for line in change_log:
        print(line)


if __name__ == "__main__":
    main()
