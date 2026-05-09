-- Migration 002: Delivery platforms, table booking platforms, image category, secondary category
-- Run in Supabase SQL Editor (Project: meridian-bristol)
-- Date: 2026-05-09

-- ── Image & secondary category ───────────────────────────────────────────────
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS image_category          text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS secondary_category      text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS secondary_category_slug text;

-- ── Delivery platforms ───────────────────────────────────────────────────────
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS delivery_deliveroo  text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS delivery_ubereats   text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS delivery_justeat    text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS delivery_foodhub    text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS delivery_beelivery  text;

-- ── Table reservation / booking platforms ────────────────────────────────────
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS booking_opentable      text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS booking_firsttable     text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS booking_resdiary       text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS booking_thefork        text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS booking_sevenrooms     text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS booking_quandoo        text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS booking_resy           text;
ALTER TABLE public.listings ADD COLUMN IF NOT EXISTS booking_designmynight  text;

-- ── Verification ─────────────────────────────────────────────────────────────
-- SELECT column_name, data_type
-- FROM information_schema.columns
-- WHERE table_schema = 'public' AND table_name = 'listings'
--   AND column_name LIKE ANY(ARRAY['image_category','secondary_%','delivery_%','booking_%'])
-- ORDER BY column_name;
