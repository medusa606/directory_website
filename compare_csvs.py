"""
compare_csvs.py — Compare two Meridian CSV files and report enrichment impact.

Analyzes differences between a baseline CSV and an enriched CSV, reporting:
  - Number of columns newly populated
  - Which columns received new data (and how many entries)
  - Breakdown by business category
  - Summary statistics
  - Random spot-check samples of enriched data (non-chains only)

Usage:
    python compare_csvs.py --before meridian_osm_baseline.csv --after meridian_osm_enriched.csv
    python compare_csvs.py --before baseline.csv --after enriched.csv --output report.txt
    python compare_csvs.py --before baseline.csv --after enriched.csv --samples 30
"""

import argparse
import sys
import random
from pathlib import Path
from collections import defaultdict

import pandas as pd


def _is_blank(val) -> bool:
    """Check if a value is considered 'blank' (empty/null/NaN)."""
    if val is None:
        return True
    s = str(val).strip().lower()
    return s in ("", "nan", "none", "null")


def compare_csvs(before_path: str, after_path: str, num_samples: int = 50) -> dict:
    """
    Compare two CSV files and identify which columns were populated.
    
    Returns a dict with enrichment statistics:
    {
        "total_rows": N,
        "columns_populated": {
            "column_name": {
                "total_entries": N,
                "by_category": {"category": count, ...}
            },
            ...
        },
        "by_category": {
            "category_name": {
                "total_rows": N,
                "populated_columns": {column: count, ...}
            },
            ...
        },
        "samples": [
            {"baseline_row": dict, "enriched_row": dict},
            ...
        ]
    }
    """
    print(f"Loading baseline CSV: {before_path}")
    df_before = pd.read_csv(before_path, dtype=str, keep_default_na=False)
    df_before = df_before.where(df_before != "", other=None)
    
    print(f"Loading enriched CSV: {after_path}")
    df_after = pd.read_csv(after_path, dtype=str, keep_default_na=False)
    df_after = df_after.where(df_after != "", other=None)
    
    print(f"  Baseline: {len(df_before):,} rows")
    print(f"  Enriched: {len(df_after):,} rows\n")
    
    # Ensure both have osm_id for matching
    if "osm_id" not in df_before.columns or "osm_id" not in df_after.columns:
        sys.exit("ERROR: Both CSVs must have 'osm_id' column for matching")
    
    # Build lookup by osm_id
    before_dict = {row["osm_id"]: row for _, row in df_before.iterrows()}
    after_dict = {row["osm_id"]: row for _, row in df_after.iterrows()}
    
    # Find common rows
    common_osm_ids = set(before_dict.keys()) & set(after_dict.keys())
    print(f"Matching rows by osm_id: {len(common_osm_ids):,}\n")
    
    # Track enrichment by column
    columns_populated = defaultdict(lambda: defaultdict(int))  # {col: {category: count}}
    by_category = defaultdict(lambda: defaultdict(int))  # {category: {column: count}}
    
    # Collect samples of enriched entries (non-chains only)
    enriched_samples = []
    total_rows_with_enrichment = 0
    
    for osm_id in common_osm_ids:
        before_row = before_dict[osm_id]
        after_row = after_dict[osm_id]
        
        category = after_row.get("category", "Unknown")
        chain_flag = after_row.get("chain_flag", "").lower()
        
        # Track if this row received any new data
        row_enriched = False
        changed_fields = []  # Track which fields changed
        
        # Compare each column
        for col in df_after.columns:
            if col in ("osm_id", "name", "category", "category_key", "category_slug",
                      "address", "city_slug", "area_slug", "business_slug",
                      "latitude", "longitude", "tags", "chain_flag", "status",
                      "ranking_tier", "source", "scrape_date", "last_synced_at",
                      "wikidata_id"):  # Exclude wikidata_id from consideration
                # Skip base columns that shouldn't change
                continue
            
            before_val = before_row.get(col)
            after_val = after_row.get(col)
            
            # Check if this column was populated (went from blank to filled)
            if _is_blank(before_val) and not _is_blank(after_val):
                columns_populated[col][category] += 1
                by_category[category][col] += 1
                row_enriched = True
                changed_fields.append(col)
        
        if row_enriched:
            total_rows_with_enrichment += 1
            
            # Collect sample if not a chain
            if chain_flag != "chain":
                enriched_samples.append({
                    "baseline_row": dict(before_row),
                    "enriched_row": dict(after_row),
                    "changed_fields": changed_fields,
                })
    
    # Randomly sample up to num_samples
    if len(enriched_samples) > num_samples:
        random.seed(42)  # Reproducible randomness
        enriched_samples = random.sample(enriched_samples, num_samples)
    
    return {
        "total_rows_matched": len(common_osm_ids),
        "total_rows_enriched": total_rows_with_enrichment,
        "columns_populated": dict(columns_populated),
        "by_category": dict(by_category),
        "samples": enriched_samples,
    }


def print_report(stats: dict, output_file: str | None = None):
    """Print a formatted enrichment report."""
    lines = []
    
    lines.append("=" * 80)
    lines.append("ENRICHMENT REPORT".center(80))
    lines.append("=" * 80)
    
    lines.append("")
    lines.append("[SUMMARY]")
    lines.append(f"  Total matched rows:    {stats['total_rows_matched']:>7,}")
    lines.append(f"  Rows with enrichment:  {stats['total_rows_enriched']:>7,}")
    if stats['total_rows_matched'] > 0:
        pct = 100.0 * stats['total_rows_enriched'] / stats['total_rows_matched']
        lines.append(f"  Enrichment rate:       {pct:>7.1f}%")
    
    lines.append("")
    lines.append("[COLUMNS POPULATED]")
    
    columns_populated = stats["columns_populated"]
    if not columns_populated:
        lines.append("  (No columns populated)")
    else:
        # Sort by total count descending
        col_counts = {col: sum(counts.values()) for col, counts in columns_populated.items()}
        for col in sorted(col_counts.keys(), key=lambda c: col_counts[c], reverse=True):
            counts = columns_populated[col]
            total = col_counts[col]
            lines.append(f"  {col:<30} {total:>5} entries")
            
            # Show breakdown by category
            for category in sorted(counts.keys()):
                count = counts[category]
                lines.append(f"    └─ {category:<26} {count:>5}")
    
    lines.append("")
    lines.append("[BREAKDOWN BY CATEGORY]")
    
    by_category = stats["by_category"]
    if not by_category:
        lines.append("  (No categories found)")
    else:
        for category in sorted(by_category.keys()):
            col_dict = by_category[category]
            total = sum(col_dict.values())
            lines.append(f"  {category:<30} ({total:>3} entries populated)")
            
            # Show which columns received data
            for col in sorted(col_dict.keys(), key=lambda c: col_dict[c], reverse=True):
                count = col_dict[col]
                lines.append(f"    ├─ {col:<26} {count:>5}")
    
    lines.append("")
    lines.append("[DATA VALIDATION SAMPLES]")
    lines.append("Comparing baseline vs enriched versions (non-chain businesses only)")
    lines.append("")
    
    samples = stats.get("samples", [])
    if not samples:
        lines.append("  (No enriched data found)")
    else:
        lines.append(f"  Showing {min(50, len(samples))} of {len(samples)} total enriched rows")
        lines.append("")
        
        for idx, sample in enumerate(samples[:50], 1):
            baseline_row = sample["baseline_row"]
            enriched_row = sample["enriched_row"]
            changed_fields = sample.get("changed_fields", [])
            
            # Print separator
            lines.append("-" * 80)
            lines.append(f"SAMPLE #{idx}  |  {enriched_row.get('name', '?')} ({enriched_row.get('category', '?')})")
            lines.append("-" * 80)
            
            # Print baseline row
            lines.append("BASELINE:")
            for key in sorted(baseline_row.keys()):
                val = str(baseline_row.get(key, "")).strip()
                if val and val.lower() not in ("", "nan", "none", "null"):
                    lines.append(f"  {key:<35} {val}")
            
            lines.append("")
            
            # Print enriched row - ONLY changed fields
            lines.append("ENRICHED (additions only):")
            if changed_fields:
                for field in sorted(changed_fields):
                    val = str(enriched_row.get(field, "")).strip()
                    if val and val.lower() not in ("", "nan", "none", "null"):
                        lines.append(f"  {field:<35} {val}")
            else:
                lines.append("  (no new data)")
            
            lines.append("")
    
    lines.append("=" * 80)
    
    # Print to stdout
    report_text = "\n".join(lines)
    print(report_text)
    
    # Also write to file if specified
    if output_file:
        with open(output_file, "w") as f:
            f.write(report_text)
        print(f"\nReport saved to: {output_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Compare two CSV files and report enrichment impact",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "--before",
        required=True,
        help="Path to baseline CSV (before enrichment)",
    )
    parser.add_argument(
        "--after",
        required=True,
        help="Path to enriched CSV (after enrichment)",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Optional: save report to file",
    )
    parser.add_argument(
        "--samples",
        type=int,
        default=50,
        help="Number of random samples to show (default: 50)",
    )
    args = parser.parse_args()
    
    before_path = Path(args.before)
    after_path = Path(args.after)
    
    if not before_path.exists():
        sys.exit(f"ERROR: --before file not found: {args.before}")
    if not after_path.exists():
        sys.exit(f"ERROR: --after file not found: {args.after}")
    
    print()
    stats = compare_csvs(str(before_path), str(after_path), num_samples=args.samples)
    print()
    print_report(stats, args.output)


if __name__ == "__main__":
    main()
