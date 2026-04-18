# Meridian Scraper — Architecture & Development Plan

> Last updated: April 2026
> Status: Approved — implementation in progress

---

## Overview

This document describes the architecture for the Meridian business data pipeline. The system collects, enriches, and publishes independent local business listings to the Meridian directory.

**Core principles:**
- OpenStreetMap (OSM) is the primary discovery source — free, bulk, UK-scalable
- Google Places is a monthly enrichment pass only (ratings + photos), staying within the free tier
- CSV files are the staging/curation/backup layer — always written before any DB push
- **No row in the database is ever overwritten.** Fields can be delta-filled into existing rows, but no existing value is ever replaced (except `google_rating` and `google_review_count` which refresh monthly)
- Non-expert users are protected: the upload script enforces all safety constraints programmatically

---

## Current State → Target Architecture

**Before:**
```
scrape_google.py → CSV → Airtable (curation) → airtable_to_supabase.py → Supabase
```

**After:**
```
┌─────────────────────────────────────────────────────────────────────┐
│ 1. DISCOVERY — scrape_osm.py                                        │
│    Overpass API (free) — bulk extract by admin boundary             │
│    Output: meridian_osm_YYYYMMDD_HHMMSS.csv                        │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
┌──────────────────────────────▼──────────────────────────────────────┐
│ 2. ENRICHMENT (all free, run sequentially or as needed)             │
│    a) enrich_socials.py          — website crawl + DuckDuckGo       │
│    b) enrich_wikidata.py         — Wikidata SPARQL                  │
│    c) enrich_companies_house.py  — trading status + address         │
│    d) enrich_fsa.py              — FSA hygiene rating               │
│    Output: *_enriched_YYYYMMDD.csv                                  │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ Human edits CSV here (curation stage)
┌──────────────────────────────▼──────────────────────────────────────┐
│ 3. UPLOAD — upload_to_supabase.py                                   │
│    Schema-aware, strict insert-only + delta-fill                    │
│    --dry-run always available before any live write                 │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ Once a month
┌──────────────────────────────▼──────────────────────────────────────┐
│ 4. GOOGLE ENRICHMENT — enrich_google.py (monthly, free tier only)  │
│    Find Place (free) → Place Details for rating + photos only       │
│    Output: google_enrichment_YYYYMM.csv → upload_to_supabase.py    │
└─────────────────────────────────────────────────────────────────────┘
```

**Legacy scripts kept untouched:**
- `airtable_to_supabase.py` — retained for potential curator workflow re-introduction
- `scrape_google.py` — Airtable push functions removed; kept for targeted Google scrapes

---

## Database Schema Migration (run once in Supabase SQL editor)

```sql
-- 1. Add osm_id as new primary logical key (partial unique index — allows NULL)
ALTER TABLE listings ADD COLUMN IF NOT EXISTS osm_id TEXT;
CREATE UNIQUE INDEX IF NOT EXISTS listings_osm_id_unique
  ON listings (osm_id) WHERE osm_id IS NOT NULL;

-- 2. Add FSA hygiene rating columns
ALTER TABLE listings ADD COLUMN IF NOT EXISTS fsa_rating TEXT;
ALTER TABLE listings ADD COLUMN IF NOT EXISTS fsa_hygiene_score INTEGER;
ALTER TABLE listings ADD COLUMN IF NOT EXISTS fsa_establishment_id TEXT;

-- 3. Ensure google_place_id is nullable
ALTER TABLE listings ALTER COLUMN google_place_id DROP NOT NULL;

-- 4. Add wikidata_id for chain detection and enrichment targeting
ALTER TABLE listings ADD COLUMN IF NOT EXISTS wikidata_id TEXT;
```

**Key point:** `upload_to_supabase.py` uses `osm_id` as the dedup key for OSM records, falling back to `google_place_id` for legacy Google-sourced records. A record needs at least one populated to be insertable.

---

## OSM Field Mapping

| Meridian column | OSM tag(s) | UK coverage est. | Notes |
|---|---|---|---|
| `name` | `name` | ~95% | Direct |
| `address` | `addr:housenumber` + `addr:street` + `addr:postcode` + `addr:city` | ~75% | Reconstructed |
| `phone` | `phone` or `contact:phone` | ~35% | Check both keys |
| `website` | `website` or `contact:website` | ~45% | Check both keys |
| `opening_hours` | `opening_hours` | ~50% | Same format as Google |
| `latitude` / `longitude` | node geometry | 100% | Direct |
| `email` | `contact:email` | ~15% | Supplemented by website crawl |
| `social_facebook` | `contact:facebook` | ~20% | |
| `social_instagram` | `contact:instagram` | ~15% | |
| `social_twitter` | `contact:twitter` | ~10% | |
| `tags` | `amenity` + `shop` + `craft` + `cuisine` | 100% | Aggregated from all keys |
| `chain_flag` | `brand` or `operator` | ~30% | Matched against chain list |
| `osm_id` | `type/id` e.g. `node/123456789` | 100% | New primary dedup key |
| `wikidata_id` | `wikidata` | ~10% | For targeted Wikidata enrichment |
| `google_rating` | ❌ not in OSM | — | Monthly Google enrichment only |
| `google_review_count` | ❌ not in OSM | — | Monthly Google enrichment only |
| `photo_url` | ❌ not in OSM | — | Monthly Google enrichment only |
| `google_place_id` | ❌ not in OSM | — | Monthly Google enrichment only |
| `fsa_rating` | ❌ not in OSM | — | FSA API enrichment (food categories) |

### OSM Category → Tag Mapping

| Meridian category | OSM tags queried |
|---|---|
| `food_produce` | `shop=bakery\|butcher\|greengrocer\|deli\|fishmonger\|cheese\|confectionery\|supermarket\|convenience` |
| `restaurants_cafes` | `amenity=restaurant\|cafe\|fast_food\|food_court` |
| `drinks_brewing` | `amenity=bar\|pub` + `craft=brewery\|distillery\|winery` + `shop=wine\|alcohol` |
| `craft_makers` | `craft=ceramics\|jeweller\|blacksmith\|weaver\|glassblower\|bookbinder\|leather\|tailor\|cobbler` |
| `art_design` | `shop=art` + `amenity=arts_centre\|art_gallery` + `craft=photographer\|sculptor` |
| `home_interiors` | `shop=furniture\|antiques\|interior_decoration\|second_hand\|vintage` |
| `plants_garden` | `shop=florist\|garden_centre` + `craft=gardener` |
| `health_wellbeing` | `amenity=spa\|massage` + `leisure=fitness_centre` + `healthcare=alternative` |

---

## Script Reference

### `scrape_osm.py` — Primary Discovery
```bash
python scrape_osm.py --area "City of Bristol"
python scrape_osm.py --area "City of Bristol" --categories food_produce,restaurants_cafes
python scrape_osm.py --area "Greater Manchester"
python scrape_osm.py --area "United Kingdom" --timeout 900
```
Uses Overpass `area` boundary — no grid, no pagination, whole city in one ~30s request. **Free, no API key.**

---

### `upload_to_supabase.py` — Safe DB Upload
```bash
python upload_to_supabase.py --file <csv> --dry-run   # always do this first
python upload_to_supabase.py --file <csv>
```
- New records: INSERT in batches of 500
- Existing records: UPDATE only NULL fields listed in `supabase_config.json`
- `google_rating` / `google_review_count`: always refreshed
- Everything else on existing rows: never touched
- Output: timestamped `upload_log_YYYYMMDD_HHMMSS.txt`

---

### `enrich_wikidata.py` — Wikidata Enrichment
```bash
python enrich_wikidata.py --file <csv>
```
For records with a `wikidata_id`, fetches: description, logo, social URLs, founding date, chain detection.
**Free, no API key. Batches QIDs for efficiency.**

---

### `enrich_companies_house.py` — Trading Status
```bash
python enrich_companies_house.py --file <csv>
```
Searches Companies House by name + postcode. Flags dissolved companies. Requires a free API key from
[developer.company-information.service.gov.uk](https://developer.company-information.service.gov.uk).
Rate limit: 600 requests / 5 minutes.

---

### `enrich_fsa.py` — Food Standards Agency Ratings
```bash
python enrich_fsa.py --file <csv>
python enrich_fsa.py --file <csv> --dry-run
```
Applies to food/drink categories only. Fetches hygiene rating, hygiene score, and FSA establishment ID.
**Free, no API key required.** ~60–70% match rate for food businesses.

---

### `enrich_google.py` — Monthly Rating + Photo Enrichment
```bash
python enrich_google.py --limit 500 --dry-run
python enrich_google.py --limit 500
python enrich_google.py --limit 500 --status published
```
Reads from Supabase where `google_place_id IS NULL`. Uses Find Place (free/unlimited) + Place Details
(5,000 free/month) to populate `google_place_id`, `google_rating`, `google_review_count`, `photo_url`.
Hard `--limit` cap prevents overspend. Checkpoint file makes runs resumable.

---

## Google Places API Pricing (Legacy API, April 2026)

| SKU | Free / month | After free tier |
|---|---|---|
| Geocoding | 10,000 | $5.00 / 1,000 |
| Find Place (ID only) | **Unlimited** | **Free** |
| Places — Nearby Search | 5,000 | $32.00 / 1,000 |
| Places — Text Search | 5,000 | $32.00 / 1,000 |
| Place Details (base) | 5,000 | $17.00 / 1,000 |
| + Contact Data | 1,000 | +$3.00 / 1,000 |
| + Atmosphere Data | 1,000 | +$5.00 / 1,000 |
| Place Photos | 1,000 | $7.00 / 1,000 |

Full Details call (all fields) = **$25.00 / 1,000 = $0.025 each** after free tier.

---

## Cost Comparison

| Task | Old (Google-first) | New (OSM-first) |
|---|---|---|
| Bristol initial discovery | ~$945 | **$0** |
| Full UK initial discovery | ~$50,000+ | **$0** |
| Monthly rating refresh (Bristol ~15k) | ~$375/month | **$0** (within 5k free tier, ~3–4 month cycle) |
| New business discovery (monthly) | ~$320/run | **$0** |
| **Estimated year 1** | **~$5,000+** | **~$0–50** |

---

## Additional Free Data Sources

| Source | Data provided | Access |
|---|---|---|
| **Food Standards Agency** | Hygiene ratings, 600k UK food businesses | Free REST API, no auth needed |
| **Companies House** | Trading status, SIC code, registered address | Free REST API, free registration |
| **Wikidata SPARQL** | Descriptions, logos, socials, chain detection | Free, no auth |
| **ONS Open Geography** | Admin boundary polygons (Bristol, wards) | Free GeoJSON download |
| **Google Knowledge Graph** | Descriptions, Wikipedia links | Free, 100,000 calls/day |
| **Historic England** | Listed building status (heritage angle) | Free API |

---

## Data Quality Expectations (OSM)

| Field | Coverage | Supplement strategy |
|---|---|---|
| Name + address | ~75–80% | — |
| Phone | ~35% | Website crawl, Companies House |
| Website | ~45% | — (key input for social enrichment) |
| Opening hours | ~50% | — |
| Email | ~15% OSM direct | ~30% via website crawl |
| Social links | ~15–20% | Website crawl, Wikidata |

Coverage gaps (newer/informal businesses) are filled by the monthly targeted Google enrichment pass.
OSM lags Google by weeks for new openings/closures — Companies House `company_status: dissolved` is the primary mitigation.

---

## Overpass API Notes

- Public endpoint: `https://overpass-api.de/api/interpreter`
- Fair use: <10,000 queries/day, <1GB/day
- Bristol full extract: ~1 query, ~5–15MB, ~30 seconds
- UK full extract: `[timeout:900]`, ~200–500MB — pipe to file
- For full UK at scale: consider self-hosted OSM PBF extract via Osmium + PostGIS on a $5/month VPS
- Geographic accuracy: Overpass `area` queries are boundary-exact — eliminates the radius-outlier problem from Google Nearby Search

---

## Files

| File | Status | Purpose |
|---|---|---|
| `scrape_osm.py` | NEW | Primary business discovery via Overpass API |
| `supabase_schema.py` | NEW | Live schema introspection utility |
| `supabase_config.json` | NEW | Delta-field and upload configuration |
| `upload_to_supabase.py` | NEW | Strict insert-only + delta-fill DB upload |
| `enrich_wikidata.py` | NEW | Wikidata SPARQL enrichment |
| `enrich_companies_house.py` | NEW | Companies House trading status |
| `enrich_fsa.py` | NEW | FSA hygiene rating enrichment |
| `enrich_google.py` | NEW | Monthly Google rating + photo enrichment |
| `enrich_socials.py` | UNCHANGED | Website crawl + DuckDuckGo social discovery |
| `airtable_to_supabase.py` | UNCHANGED | Retained for future curator workflow |
| `scrape_google.py` | MODIFIED | Airtable push removed; kept for targeted Google scrapes |

---

## Environment Variables

```env
# Required for all scripts
GOOGLE_MAPS_API_KEY=...
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=...

# Required for enrich_companies_house.py
COMPANIES_HOUSE_API_KEY=...

# Legacy — kept for airtable_to_supabase.py only
AIRTABLE_API_KEY=...
AIRTABLE_BASE_ID=...
AIRTABLE_CANDIDATES_TABLE_NAME=Candidates
```

---

## Verification Checklist

- [ ] Run Supabase migration SQL — confirm `osm_id` index created, `google_place_id` nullable
- [ ] `python supabase_schema.py` — prints live DB columns in schema order
- [ ] `python scrape_osm.py --area "City of Bristol" --dry-run` — prints count + sample, no writes
- [ ] `python scrape_osm.py --area "City of Bristol"` — CSV columns match Supabase schema
- [ ] `python enrich_fsa.py --file <csv> --dry-run` — shows FSA match rate
- [ ] `python upload_to_supabase.py --file <csv> --dry-run` — correct insert/delta/skip counts
- [ ] `python upload_to_supabase.py --file <csv>` — records in Supabase, nothing overwritten
- [ ] Re-upload same CSV — all rows skip (idempotent)
- [ ] Re-upload enriched CSV — only NULL fields filled, core data untouched
- [ ] Add new column to Supabase → re-run upload — interactive prompt fires, saved to config
- [ ] `python enrich_google.py --limit 10 --dry-run` — shows records + cost estimate
