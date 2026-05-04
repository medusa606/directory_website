-- ============================================================
-- Meridian Directory — Curation & Owner Portal Tables
-- Run once in your Supabase SQL editor (Dashboard → SQL Editor)
-- ============================================================

-- ── 1. listing_locks ─────────────────────────────────────────
-- Pessimistic locking: one curator can edit a listing at a time.
-- Locks expire after 10 minutes (cleaned up on app init).
CREATE TABLE IF NOT EXISTS public.listing_locks (
  listing_id      uuid NOT NULL REFERENCES public.listings(id) ON DELETE CASCADE,
  locked_by_email text NOT NULL,
  locked_by_id    uuid NOT NULL,
  locked_at       timestamptz NOT NULL DEFAULT now(),
  CONSTRAINT listing_locks_pkey PRIMARY KEY (listing_id)
);

-- ── 2. curation_audit ────────────────────────────────────────
-- Immutable log of every change made by a curator or approved submission.
CREATE TABLE IF NOT EXISTS public.curation_audit (
  id            uuid    NOT NULL DEFAULT gen_random_uuid(),
  listing_id    uuid    NOT NULL REFERENCES public.listings(id) ON DELETE CASCADE,
  curator_email text    NOT NULL,
  curator_id    uuid    NOT NULL,
  changed_at    timestamptz NOT NULL DEFAULT now(),
  changes       jsonb   NOT NULL,  -- { field: { before, after }, ... }
  source        text    NOT NULL DEFAULT 'curator', -- 'curator' | 'owner_submission' | 'trigger'
  submission_id uuid,              -- FK to owner_submissions if applicable
  CONSTRAINT curation_audit_pkey PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS idx_curation_audit_listing
  ON public.curation_audit(listing_id);
CREATE INDEX IF NOT EXISTS idx_curation_audit_curator
  ON public.curation_audit(curator_id, changed_at DESC);

-- ── 3. owner_profiles ────────────────────────────────────────
-- Links a Supabase auth user to a verified business listing.
-- A curator must approve the claim before the owner gets edit access.
CREATE TABLE IF NOT EXISTS public.owner_profiles (
  id           uuid NOT NULL DEFAULT gen_random_uuid(),
  user_id      uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  listing_id   uuid REFERENCES public.listings(id) ON DELETE SET NULL,
  claim_status text NOT NULL DEFAULT 'pending', -- pending | approved | rejected
  claimed_at   timestamptz NOT NULL DEFAULT now(),
  reviewed_by  text,
  reviewed_at  timestamptz,
  reject_note  text,
  CONSTRAINT owner_profiles_pkey     PRIMARY KEY (id),
  CONSTRAINT owner_profiles_user_key UNIQUE (user_id)
);

CREATE INDEX IF NOT EXISTS idx_owner_profiles_listing
  ON public.owner_profiles(listing_id);
CREATE INDEX IF NOT EXISTS idx_owner_profiles_status
  ON public.owner_profiles(claim_status);

-- ── 4. owner_submissions ─────────────────────────────────────
-- Staged proposed changes submitted by business owners.
-- Curators review and approve/reject each submission.
CREATE TABLE IF NOT EXISTS public.owner_submissions (
  id                  uuid NOT NULL DEFAULT gen_random_uuid(),
  listing_id          uuid NOT NULL REFERENCES public.listings(id) ON DELETE CASCADE,
  owner_user_id       uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  owner_email         text,
  submitted_at        timestamptz NOT NULL DEFAULT now(),
  status              text NOT NULL DEFAULT 'pending', -- pending | approved | rejected
  proposed_fields     jsonb,      -- { founders_story, logo_url, founders_image, ... }
  proposed_image_urls text[],
  curator_notes       text,
  reviewed_by         text,
  reviewed_at         timestamptz,
  CONSTRAINT owner_submissions_pkey PRIMARY KEY (id)
);

CREATE INDEX IF NOT EXISTS idx_owner_submissions_listing
  ON public.owner_submissions(listing_id);
CREATE INDEX IF NOT EXISTS idx_owner_submissions_status
  ON public.owner_submissions(status, submitted_at DESC);

-- ============================================================
-- RLS Policies
-- ============================================================

-- ── listings ─────────────────────────────────────────────────
ALTER TABLE public.listings ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "listings_anon_read"       ON public.listings;
DROP POLICY IF EXISTS "listings_auth_read"        ON public.listings;
DROP POLICY IF EXISTS "listings_curator_update"   ON public.listings;

-- Public read access (your existing directory website)
CREATE POLICY "listings_anon_read" ON public.listings
  FOR SELECT TO anon USING (true);

-- Authenticated read (curator tool)
CREATE POLICY "listings_auth_read" ON public.listings
  FOR SELECT TO authenticated USING (true);

-- Only curators can update listings
-- Set app_metadata.role = 'curator' on curator accounts in the Supabase Auth dashboard
CREATE POLICY "listings_curator_update" ON public.listings
  FOR UPDATE TO authenticated
  USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'curator');

-- ── listing_locks ─────────────────────────────────────────────
ALTER TABLE public.listing_locks ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "locks_auth_read"   ON public.listing_locks;
DROP POLICY IF EXISTS "locks_own_insert"  ON public.listing_locks;
DROP POLICY IF EXISTS "locks_own_delete"  ON public.listing_locks;

CREATE POLICY "locks_auth_read" ON public.listing_locks
  FOR SELECT TO authenticated USING (true);

CREATE POLICY "locks_own_insert" ON public.listing_locks
  FOR INSERT TO authenticated
  WITH CHECK (locked_by_id = auth.uid());

CREATE POLICY "locks_own_delete" ON public.listing_locks
  FOR DELETE TO authenticated
  USING (locked_by_id = auth.uid());

-- ── curation_audit ─────────────────────────────────────────────
ALTER TABLE public.curation_audit ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "audit_auth_read"  ON public.curation_audit;
DROP POLICY IF EXISTS "audit_own_insert" ON public.curation_audit;

CREATE POLICY "audit_auth_read" ON public.curation_audit
  FOR SELECT TO authenticated USING (true);

CREATE POLICY "audit_own_insert" ON public.curation_audit
  FOR INSERT TO authenticated
  WITH CHECK (curator_id = auth.uid());

-- ── owner_profiles ─────────────────────────────────────────────
ALTER TABLE public.owner_profiles ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "owner_profiles_own"            ON public.owner_profiles;
DROP POLICY IF EXISTS "owner_profiles_curator_read"   ON public.owner_profiles;
DROP POLICY IF EXISTS "owner_profiles_curator_update" ON public.owner_profiles;

-- Owners can view and insert their own profile (one per user)
CREATE POLICY "owner_profiles_own" ON public.owner_profiles
  FOR ALL TO authenticated
  USING  (user_id = auth.uid())
  WITH CHECK (user_id = auth.uid());

-- Curators can read all profiles
CREATE POLICY "owner_profiles_curator_read" ON public.owner_profiles
  FOR SELECT TO authenticated
  USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'curator');

-- Curators can update profiles (to approve/reject claims)
CREATE POLICY "owner_profiles_curator_update" ON public.owner_profiles
  FOR UPDATE TO authenticated
  USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'curator');

-- ── owner_submissions ─────────────────────────────────────────
ALTER TABLE public.owner_submissions ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "submissions_own"            ON public.owner_submissions;
DROP POLICY IF EXISTS "submissions_curator_read"   ON public.owner_submissions;
DROP POLICY IF EXISTS "submissions_curator_update" ON public.owner_submissions;

-- Owners can view and insert their own submissions
CREATE POLICY "submissions_own" ON public.owner_submissions
  FOR ALL TO authenticated
  USING  (owner_user_id = auth.uid())
  WITH CHECK (owner_user_id = auth.uid());

-- Curators can read all submissions
CREATE POLICY "submissions_curator_read" ON public.owner_submissions
  FOR SELECT TO authenticated
  USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'curator');

-- Curators can update submissions (approve/reject)
CREATE POLICY "submissions_curator_update" ON public.owner_submissions
  FOR UPDATE TO authenticated
  USING ((auth.jwt() -> 'app_metadata' ->> 'role') = 'curator');

-- ============================================================
-- Postgres Trigger: Tamper-proof audit trail
-- Fires after any UPDATE on listings, captures diffs.
-- auth.uid() / auth.email() work inside triggers when the
-- call comes through PostgREST (Supabase API).
-- ============================================================
CREATE OR REPLACE FUNCTION public.fn_listings_audit_trigger()
RETURNS TRIGGER
LANGUAGE plpgsql
SECURITY DEFINER
SET search_path = public
AS $$
DECLARE
  v_curator_id    uuid;
  v_curator_email text;
  v_changes       jsonb;
BEGIN
  BEGIN
    v_curator_id    := (auth.jwt() ->> 'sub')::uuid;
    v_curator_email := coalesce(auth.jwt() ->> 'email', 'system');
  EXCEPTION WHEN others THEN
    v_curator_id    := '00000000-0000-0000-0000-000000000000'::uuid;
    v_curator_email := 'system';
  END;

  -- Build diff: only include columns that actually changed
  SELECT jsonb_object_agg(
    kv_new.key,
    jsonb_build_object('before', kv_old.value, 'after', kv_new.value)
  ) INTO v_changes
  FROM  jsonb_each(to_jsonb(OLD)) AS kv_old
  JOIN  jsonb_each(to_jsonb(NEW)) AS kv_new ON kv_old.key = kv_new.key
  WHERE kv_old.value IS DISTINCT FROM kv_new.value
    AND kv_old.key NOT IN (
      'id', 'last_synced_at', 'scrape_date', 'illustration_generated_at'
    );

  IF v_changes IS NOT NULL AND v_changes <> '{}'::jsonb THEN
    INSERT INTO public.curation_audit
      (listing_id, curator_email, curator_id, changes, source)
    VALUES
      (NEW.id, v_curator_email, v_curator_id, v_changes, 'trigger');
  END IF;

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_listings_audit ON public.listings;
CREATE TRIGGER trg_listings_audit
  AFTER UPDATE ON public.listings
  FOR EACH ROW
  EXECUTE FUNCTION public.fn_listings_audit_trigger();
