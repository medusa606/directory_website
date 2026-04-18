"""
supabase_schema.py — Meridian Directory
========================================
Runtime schema introspection utility. Queries the live Supabase database
to return the column definitions for the listings table.

All other scripts import from this module so that CSV column ordering and
field awareness always stays in sync with the actual DB schema.

Usage (standalone — prints columns):
    python supabase_schema.py

Usage (as a module):
    from supabase_schema import get_schema, get_column_names
    columns = get_schema()        # list of (column_name, data_type)
    names   = get_column_names()  # list of column name strings
"""

import os
import sys
import json
from pathlib import Path

from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

_SUPABASE_URL = os.getenv("SUPABASE_URL")
_SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
_CONFIG_PATH  = Path(__file__).parent / "supabase_config.json"


def _load_config() -> dict:
    if _CONFIG_PATH.exists():
        with open(_CONFIG_PATH) as f:
            return json.load(f)
    return {"listings_table": "listings"}


def _get_client() -> Client:
    if not _SUPABASE_URL or not _SUPABASE_KEY:
        sys.exit(
            "ERROR: SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY must be set in .env"
        )
    return create_client(_SUPABASE_URL, _SUPABASE_KEY)


def get_schema(table: str | None = None) -> list[tuple[str, str]]:
    """Return ordered list of (column_name, data_type) for the listings table.

    Queries information_schema.columns via the Supabase REST API using the
    service role key so RLS is bypassed.
    """
    config = _load_config()
    table_name = table or config.get("listings_table", "listings")
    client = _get_client()

    response = (
        client.table("information_schema.columns")
        .select("column_name,data_type,ordinal_position")
        .eq("table_schema", "public")
        .eq("table_name", table_name)
        .order("ordinal_position")
        .execute()
    )

    if not response.data:
        # information_schema may not be directly queryable via PostgREST;
        # fall back to a raw SQL RPC if available, or return empty list with warning.
        print(
            f"WARNING: Could not read schema for '{table_name}' via REST. "
            "Ensure the service role key is used and the table exists. "
            "Falling back to config-derived column list.",
            file=sys.stderr,
        )
        return _fallback_columns(config)

    return [(row["column_name"], row["data_type"]) for row in response.data]


def get_column_names(table: str | None = None) -> list[str]:
    """Return ordered list of column names for the listings table."""
    return [name for name, _ in get_schema(table)]


def _fallback_columns(config: dict) -> list[tuple[str, str]]:
    """Build a best-effort column list from supabase_config.json when live
    schema query is unavailable. Returns (name, 'unknown') tuples."""
    all_fields = (
        config.get("known_non_delta_fields", [])
        + config.get("delta_fill_fields", [])
        + config.get("refresh_always_fields", [])
    )
    # Deduplicate preserving order
    seen = set()
    unique = []
    for f in all_fields:
        if f not in seen:
            seen.add(f)
            unique.append(f)
    return [(f, "unknown") for f in unique]


def check_for_new_columns(existing_columns: list[str]) -> None:
    """Detect columns present in the live DB but absent from supabase_config.json.

    For each unknown column, prompt the user interactively whether it should be
    treated as a delta-fill field. Saves the answer back to supabase_config.json.
    Non-interactive environments (no TTY) skip the prompt silently.
    """
    if not _CONFIG_PATH.exists():
        return

    with open(_CONFIG_PATH) as f:
        config = json.load(f)

    known = set(
        config.get("primary_keys", [])
        + config.get("delta_fill_fields", [])
        + config.get("refresh_always_fields", [])
        + config.get("known_non_delta_fields", [])
    )

    new_cols = [c for c in existing_columns if c not in known]
    if not new_cols:
        return

    if not sys.stdin.isatty():
        print(
            f"INFO: {len(new_cols)} new DB column(s) not in supabase_config.json: "
            f"{new_cols}. Run interactively to classify them.",
            file=sys.stderr,
        )
        return

    changed = False
    for col in new_cols:
        answer = input(
            f"\nNew DB column detected: '{col}'\n"
            f"Add to delta-fill fields (fill NULL values only on existing rows)? [y/N] "
        ).strip().lower()
        if answer == "y":
            config["delta_fill_fields"].append(col)
            print(f"  → Added '{col}' to delta_fill_fields.")
        else:
            config["known_non_delta_fields"].append(col)
            print(f"  → Added '{col}' to known_non_delta_fields (never updated).")
        changed = True

    if changed:
        with open(_CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=2)
        print(f"Saved updated config to {_CONFIG_PATH}")


if __name__ == "__main__":
    print("Fetching live schema from Supabase...\n")
    schema = get_schema()
    if not schema:
        print("No columns returned. Check credentials and table name in supabase_config.json.")
        sys.exit(1)
    print(f"{'Column':<35} {'Type'}")
    print("-" * 55)
    for col, dtype in schema:
        print(f"{col:<35} {dtype}")
    print(f"\nTotal: {len(schema)} columns")
