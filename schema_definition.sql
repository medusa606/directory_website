-- Meridian Directory - Supabase Schema Definition
-- Synced from live DB: 2026-04-20
-- This is the canonical schema reference — keep in sync with Supabase

create table public.listings (
  id uuid not null default gen_random_uuid (),
  name text not null,
  category text null,
  address text null,
  latitude double precision null,
  longitude double precision null,
  phone text null,
  website text null,
  google_maps_url text null,
  photo_url text null,
  google_photo_reference text null,
  google_summary text null,
  opening_hours text null,
  google_rating real null,
  google_review_count integer null,
  google_place_id text null,
  source text null,
  scrape_date text null,
  status text null,
  chain_flag text null,
  editor_notes text null,
  story_draft text null,
  description text null,
  tags text[] null,
  is_featured boolean null,
  image_url text null,
  category_key text null,
  last_synced_at text null,
  ranking_tier text null default 'standard'::text,
  category_slug text null,
  city_slug text null,
  area_slug text null,
  business_slug text null,
  email text null,
  social_facebook text null,
  social_instagram text null,
  social_twitter text null,
  social_tiktok text null,
  social_linkedin text null,
  social_youtube text null,
  add_listing_illustration boolean null default false,
  illustration_status character varying null,
  illustration_url text null,
  illustration_source_photo text null,
  illustration_generated_at timestamp with time zone null,
  founders_story text null,
  founders_image text null,
  logo_url text null,
  show_logo boolean null default false,
  osm_id text null,
  wikidata_id text null,
  fsa_rating text null,
  fsa_hygiene_score text null,
  fsa_establishment_id text null,
  constraint listings_pkey primary key (id),
  constraint listings_google_place_id_key unique (google_place_id)
) TABLESPACE pg_default;

create unique INDEX IF not exists idx_listing_slugs on public.listings using btree (city_slug, area_slug, business_slug) TABLESPACE pg_default;

create unique INDEX IF not exists idx_listings_osm_id on public.listings using btree (osm_id) TABLESPACE pg_default
where
  (osm_id is not null);

-- COLUMN COUNT: 55 (including id)
-- CRITICAL VALIDATION RULES FOR CSV IMPORT
-- 1. 'name' is NOT NULL - every row MUST have a business name
-- 2. 'google_place_id' is UNIQUE - no duplicates allowed
-- 3. 'osm_id' is UNIQUE (where not null)
-- 4. 'id' is PRIMARY KEY - will be auto-generated if not provided
-- 5. (city_slug, area_slug, business_slug) composite unique index
-- 4. Numeric fields (latitude, longitude, google_rating) should contain only numbers
-- 5. Boolean fields (is_featured, show_logo) accept: true/false, 1/0, or NULL
-- 6. Array fields (tags) format: ["tag1", "tag2"] or NULL
-- 7. Timestamp: ISO 8601 format (YYYY-MM-DD HH:MM:SS) or NULL
-- ═══════════════════════════════════════════════════════════════════════════════
