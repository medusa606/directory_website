# Curation & Owner Portal — Deployment Guide

## What was built

| File | Purpose |
|---|---|
| `migrations/001_curation_tables.sql` | Run once in Supabase SQL Editor |
| `curator/index.html` | Curator portal — authenticated editing UI |
| `owner/index.html` | Business owner portal — claim + submit changes |

---

## Step 1 — Run the SQL migration

1. Open **Supabase Dashboard → SQL Editor → New Query**
2. Paste the full contents of `migrations/001_curation_tables.sql`
3. Click **Run**

This creates:

- `listing_locks` — prevents concurrent edits (primary key on `listing_id`)
- `curation_audit` — immutable log of every change with curator identity + diff
- `owner_profiles` — links an auth user to a verified business listing
- `owner_submissions` — staged owner-proposed changes awaiting curator review
- Row Level Security policies on all tables (including `listings`)
- A Postgres trigger that auto-logs all `listings` updates as a tamper-proof safety net

---

## Step 2 — Create curator accounts in Supabase Auth

1. Go to **Supabase Dashboard → Authentication → Users → Add User**
2. Create an email/password account for each curator (up to 10)
3. After creating each account, click the user → **Edit user** → expand **Custom Claims (app\_metadata)**
4. Set the following JSON value: `{ "role": "curator" }`
5. Save

Without this `app_metadata.role` claim, the curator portal login will reject the user even with valid credentials.

---

## Step 3 — Create Supabase Storage bucket for owner image uploads

1. Go to **Supabase Dashboard → Storage → New Bucket**
2. Name: `owner-images`
3. Set **Public bucket**: ✓ (so uploaded images are publicly readable by the directory website)
4. Add the following Storage policies via **SQL Editor**:

```sql
-- Allow authenticated users to upload into their own folder
CREATE POLICY "owner_images_upload"
  ON storage.objects FOR INSERT TO authenticated
  WITH CHECK (
    bucket_id = 'owner-images'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

-- Allow authenticated users to delete their own uploads
CREATE POLICY "owner_images_delete"
  ON storage.objects FOR DELETE TO authenticated
  USING (
    bucket_id = 'owner-images'
    AND (storage.foldername(name))[1] = auth.uid()::text
  );

-- Public read access
CREATE POLICY "owner_images_public_read"
  ON storage.objects FOR SELECT TO anon
  USING (bucket_id = 'owner-images');
```

---

## Step 4 — Deploy to Cloudflare Pages

Each portal is a plain HTML file with no build step. Deploy each as a **separate Cloudflare Pages project** on your existing free account.

**Free tier gives you:**
- Unlimited Pages projects per account
- A free `*.pages.dev` subdomain per project
- Free custom subdomain attachment to any domain already on your account (e.g. `curator.yourdomain.com`) — just a DNS CNAME, no new domain registration needed

### Option A — Wrangler CLI (recommended)

```bash
# Install Wrangler if you haven't already
npm install -g wrangler

# Deploy the curator portal
npx wrangler pages deploy curator/ \
  --project-name meridian-curator \
  --branch main
# → https://meridian-curator.pages.dev

# Deploy the owner portal
npx wrangler pages deploy owner/ \
  --project-name meridian-owners \
  --branch main
# → https://meridian-owners.pages.dev
```

### Option B — Cloudflare Dashboard (drag & drop)

1. **Cloudflare Dashboard → Pages → Create a project → Direct Upload**
2. Upload the `curator/` directory → set project name `meridian-curator`
3. Repeat for `owner/` → project name `meridian-owners`
4. No build configuration needed — the HTML file is served directly

### Add custom subdomains (free, no new domain needed)

If your domain is already on Cloudflare (e.g. `yourdomain.com`):

1. Go to the Pages project → **Custom domains → Set up a custom domain**
2. Enter `curator.yourdomain.com` → Cloudflare auto-creates the DNS CNAME record
3. Repeat for `owners.yourdomain.com`

---

## Step 5 — Protect the curator portal with Cloudflare Access (recommended)

Add a second authentication gate in front of the curator portal so only approved email addresses can even load the page, before they reach the Supabase login.

**Free for up to 50 users.**

1. **Cloudflare Dashboard → Zero Trust → Access → Applications → Add an application**
2. Select **Self-hosted**
3. Application domain: `curator.yourdomain.com` (or `meridian-curator.pages.dev`)
4. Add a policy: **Allow → Emails → paste your curators' email addresses**
5. Save

Anyone not on the list gets a Cloudflare block page and never reaches the HTML.

---

## Step 6 — How concurrent editing works

The `listing_locks` table uses `listing_id` as a **primary key**, so only one lock per listing can exist at any time.

| Action | What happens |
|---|---|
| Curator clicks **Edit** | Upserts a lock row. If another curator's lock exists, shows a 🔒 banner and disables editing. |
| Curator saves or cancels | Lock row is deleted immediately. |
| Curator navigates to another listing | Lock is released before moving. |
| Tab or window is closed | `navigator.sendBeacon` fires a best-effort DELETE. |
| Lock older than 10 minutes | Purged automatically on next app load by any curator. |
| Lock heartbeat | Refreshed every 4 minutes while an edit panel is open. |

---

## Step 7 — Curator workflow

1. Sign in at `curator.yourdomain.com` with email + password
2. Browse listings using the filter bar (**No Story**, **No Tags**, **No Image**, **No Desc**, status filters)
3. Use the search box to jump to a specific business by name or area
4. Click **Edit** on a listing → acquires a lock, opens the edit panel
5. Make changes (category, tags, description, founder's story, socials, contact info, etc.)
6. Click **Save to Database** → writes directly to `listings` + logs to `curation_audit`
7. The card auto-advances to the next listing after saving
8. Click the **📥 Submissions** filter to review owner-proposed changes — see a diff of current vs proposed, then approve (applies changes) or reject with a note
9. Click the **🏢 Claims** filter to approve or reject business owner claim requests

---

## Step 8 — Owner workflow

1. Business owner visits `owners.yourdomain.com`
2. Creates an account (email + password or magic link)
3. Searches for their business by name → clicks **Claim**
4. A curator receives the claim in the **Claims** tab and approves or rejects it
5. Once approved, the owner sees their live listing data and can edit:
   - Founder's story (up to 1500 chars)
   - Logo URL
   - Founder's photo URL
   - Up to 3 uploaded images (stored in Supabase Storage `owner-images` bucket)
6. Owner clicks **Submit for Review** → writes to `owner_submissions` only (owners never write to `listings` directly)
7. Curator reviews the diff in the **Submissions** tab → approve or reject with note
8. On approval: proposed fields are applied to `listings` and logged in `curation_audit` with `source = 'owner_submission'`
9. Owner can view all their past submissions and their status (pending / approved / rejected) in the Submission History section

---

## Audit log queries

Every change is recorded in `curation_audit` with a JSONB diff of `{ field: { before, after } }`.

```sql
-- Recent changes across all listings
SELECT curator_email, listing_id, changed_at, source, changes
FROM curation_audit
ORDER BY changed_at DESC
LIMIT 50;

-- Full history for a specific listing
SELECT curator_email, changed_at, source, changes
FROM curation_audit
WHERE listing_id = '<uuid>'
ORDER BY changed_at DESC;

-- All changes made by a specific curator
SELECT listing_id, changed_at, changes
FROM curation_audit
WHERE curator_email = 'curator@example.com'
ORDER BY changed_at DESC;

-- Changes approved from owner submissions
SELECT listing_id, curator_email, changed_at, submission_id
FROM curation_audit
WHERE source = 'owner_submission'
ORDER BY changed_at DESC;
```

The Postgres trigger (`trg_listings_audit`) also auto-logs every direct `UPDATE` on `listings` as a tamper-proof fallback, even if the API call bypasses the frontend.

---

## RLS policy summary

| Table | `anon` | Authenticated owner (own rows) | Curator |
|---|---|---|---|
| `listings` | SELECT | SELECT | SELECT + UPDATE |
| `listing_locks` | — | SELECT | SELECT + INSERT own + DELETE own |
| `curation_audit` | — | SELECT | SELECT + INSERT own |
| `owner_profiles` | — | ALL own row | SELECT + UPDATE |
| `owner_submissions` | — | ALL own rows | SELECT + UPDATE |

Curators are identified by `app_metadata.role = 'curator'` in the Supabase JWT. Owners have no special role — RLS isolates their data by `user_id = auth.uid()`.
