# Category Slugs Consolidation Analysis

## Overview
This document proposes consolidation of duplicate and near-duplicate category slug entries. The goal is to eliminate spelling variations, semantic redundancy, and conflicting entries while preserving meaningful distinctions.

---

## Consolidation Proposals by Category

### **Cafes**
**Current:** `cafe`, `coffee_shop`, `coffee`, `tea`, `bubble_tea`, `brunch`, `juice`

| Action | Current | Proposed | Reason |
|--------|---------|----------|--------|
| KEEP | cafe | cafe | Primary category |
| CONSOLIDATE | coffee_shop, coffee | coffee | "coffee_shop" is redundant |
| KEEP | tea | tea | Distinct offering (tea-focused) |
| KEEP | bubble_tea | bubble_tea | Distinct offering |
| REMOVE | brunch | — | Make optional tag instead of category slug |
| REMOVE | juice | — | Belongs in Food & Produce, not Cafes |

**Proposed list:** `cafe`, `coffee`, `tea`, `bubble_tea`

---

### **Restaurants & Fast Food**
**Current:** `restaurant`, `fast_food`, `takeaway`, `ice_cream`

| Action | Current | Proposed | Reason |
|--------|---------|----------|--------|
| KEEP | restaurant | restaurant | Primary |
| KEEP | fast_food | fast_food | Primary |
| KEEP | takeaway | takeaway | Service model |
| KEEP | ice_cream | ice_cream | Gelaterie/ice cream parlor is a distinct venue |

**Proposed list:** `restaurant`, `fast_food`, `takeaway`, `ice_cream` 

---

### **Food & Produce**
**Current:** 20 entries (longest list, many duplicates)

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Greengrocers | `produce`, `veg`, `vegetables` | `greengrocer` | Consolidate variations; "greengrocer" is the standard term |
| Bakery | `bakery`, `cake`, `donut`, `flapjacks` | `bakery` | Consolidate to primary; other items are products |
| Deli | `deli`, `delicatessen` | `deli` | Consolidate spelling variation |
| Sweets | `sweet_shop`, `sweets`, `confectionery`, `candy` | `confectionery` | Consolidate to most standard British term |
| Dairy | `cheesemonger` | `cheesemonger` | Specialist shop; remove generic `cheese` |
| Convenience | `supermarket`, `corner_shop`, `convenience_store` | `supermarket`, `convenience_store` | Remove `corner_shop` (covered by convenience) |
**Proposed list:** `greengrocer`, `bakery`, `deli`, `confectionery`, `cheesemonger`, `supermarket`, `convenience_store`

---

### **Drinks & Brewing**
**Current:** 14 entries

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Pub | `pub` | `pub` | KEEP |
| Taproom | `taproom` | `taproom` | Modern brewery bar |
| Wine Bar | `wine_bar` | `wine_bar` | KEEP |
| Cocktail Bar | `cocktail_bar` | `cocktail_bar` | KEEP |
| Off-licence | `off_licence` | `off_licence` | UK British spelling |
| Brewery | `brewery` | `brewery` | KEEP |
| Remove | `bar`, `tavern`, `bottle_shop`, `liquor_store`, `microbrewery`, `cellar`, `wine` | — | Consolidate or too vague |

**Proposed list:** `pub`, `taproom`, `wine_bar`, `cocktail_bar`, `off_licence`, `brewery`

---

### **Health & Wellbeing**
**Current:** 25 entries (mixed services and service types)

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Spa/Wellness | `spa`, `sauna`, `steam_room` | KEEP ALL | Distinct experiences |
| Therapy | `massage`, `therapist`, `yoga`, `pilates`, `meditation`, `wellness`, `acupuncture`, `chiropractor`, `osteopath` | KEEP ALL | Each is distinct service |
| Pharmacy | `pharmacy`, `chemist`, `dispensary` | `pharmacy` | Consolidate variations (pharmacy is standard) |
| Dentist | `dentist`, `dental` | `dentist` | Consolidate (dentist is standard) |
| Hair | `hairdresser`, `hair_salon`, `salon`, `barbershop`, `barber` | `hairdresser`, `barber` | Remove `hair_salon`, `salon`, `barbershop` (redundant) |
| Nails | `nail_salon`, `nails`, `manicure`, `pedicure` | `nail_salon` | Consolidate; manicure/pedicure are services not types |

**Proposed list:** `spa`, `sauna`, `steam_room`, `massage`, `therapist`, `yoga`, `pilates`, `meditation`, `wellness`, `acupuncture`, `chiropractor`, `osteopath`, `pharmacy`, `dentist`, `hairdresser`, `barber`, `nail_salon`

---

### **Fitness & Sports**
**Current:** 30+ entries

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Gym | `gym` | `gym` | KEEP; remove `fitness`, `crossfit`, `personal_trainer` |
| Swimming | `swimming`, `pool`, `swimming_pool` | `swimming_pool` | Consolidate variations |
| Golf | `golf`, `golf_course` | `golf_course` | Consolidate (golf_course is specific) |
| Climbing | `climbing`, `climbing_wall` | `climbing_wall` | Consolidate (wall is specific) |
| Karting | `karting`, `go_kart`, `kart_racing` | `karting` | Consolidate to standard |
| Padel | `padel`, `padel_tennis` | `padel` | Consolidate |
| Cycling | `cycling`, `bike_shop`, `bicycle` | `bike_shop` | Bike shop is the venue |
| Sports Venues | `sports_centre`, `leisure_centre`, `leisure_center` | `sports_centre` | Consolidate; remove British/American spelling duplicate |
| Clubs | `sports_club`, `rugby`, `football_club`, `tennis_club` | `sports_club` | Consolidate (sports_club is umbrella) |
| Watersports | `watersports` | `watersports` | Covers kayak, sailing, canoeing, etc. |
| Remove | `outdoor`, `outdoor_activities`, `hiking`, `kayak`, `canoeing`, `sailing` | — | Not business-related or covered by watersports |

**Proposed list:** `gym`, `swimming_pool`, `golf_course`, `climbing_wall`, `karting`, `padel`, `bike_shop`, `sports_centre`, `sports_club`, `watersports`

---

### **Entertainment**
**Current:** 7 entries

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Theatre | `theatre`, `theater` | `theatre` | Consolidate to British spelling (standardise) |
| Live Music | `live_music`, `music_venue` | `music_venue` | Consolidate |
| Nightlife | `nightclub`, `club` | `nightclub` | Consolidate |
| Cinema | `cinema` | `cinema` | KEEP |

**Proposed list:** `cinema`, `theatre`, `music_venue`, `nightclub`

---

### **Art & Design**
**Current:** 9 entries

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Gallery | `gallery`, `arts_centre` | KEEP BOTH | Distinct (gallery=exhibition, arts_centre=hub) |
| Studio | `studio` | `studio` | KEEP |
| Photography | `photographer`, `photography_studio`, `photography` | `photography_studio` | Consolidate variations |
| Visual Art | `painter`, `artist` | `artist` | Consolidate (painter is specific type) |
| Music | `music_school`, `music_academy`, `music_studio` | `music_school` | Consolidate variations |
| Dance | `dance_studio`, `dance`, `dance_school` | `dance_studio` | Consolidate variations |

**Proposed list:** `gallery`, `arts_centre`, `studio`, `photography_studio`, `artist`, `music_school`, `dance_studio`

---

### **Craft & Makers**
**Current:** 6 entries

✅ **No consolidation needed** — all are distinct craft types.

**Proposed list:** `pottery`, `ceramics`, `weaving`, `textiles`, `knitting`, `sewing`

---

### **Plants & Garden**
**Current:** 10 entries

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Florist | `florist`, `flowers`, `floristry` | `florist` | Consolidate variations |
| Garden Centre | `garden_centre`, `nursery` | KEEP BOTH | Distinct (centre sells ready-made, nursery grows) |
| Landscaping | `landscaping`, `landscaper`, `groundskeeper` | `landscaping` | Consolidate; landscaping is the service |
| Garden | `garden`, `lawn` | `garden` | Consolidate |

**Proposed list:** `florist`, `garden_centre`, `nursery`, `landscaping`, `garden`

---

### **Home & Interiors**
**Current:** 21 entries (very mixed)

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Antiques | `antiques`, `vintage` | KEEP | Remove `secondhand` (market overlap) |
| Flooring | `carpet`, `carpet_shop`, `rugs`, `flooring` | `carpet`, `flooring` | Consolidate carpet variations |
| Lighting | `lighting`, `lighting_shop`, `lamps` | `lighting` | Consolidate variations |
| Paint | `paint_supplies`, `paint_shop` | `paint_supplies` | Consolidate |
| Tiles | `tile_shop`, `tiles`, `tiling` | `tiles` | Consolidate variations |
| Furniture | `sofa`, `sofa_shop`, `sofas`, `couch` | `furniture` | Consolidate (too granular) |
| Interiors/Homeware | `interiors`, `furniture`, `home_goods`, `homeware` | `furniture`, `homeware` | Consolidate variations |
| Decorating | `decorating` | `decorating` | KEEP |

**Proposed list:** `antiques`, `vintage`, `carpet`, `flooring`, `lighting`, `paint_supplies`, `tiles`, `furniture`, `homeware`, `decorating`

---

### **Services**
**Current:** 9 entries

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Laundry | `launderette`, `laundromat`, `laundrette` | `launderette` | Consolidate British spelling variations (laundromat is US) |
| Dry Cleaning | `dry_cleaning` | `dry_cleaning` | KEEP |
| Alterations | `tailor`, `alterations` | `tailor` | Consolidate (tailor does alterations) |
| Charity | `charity_shop`, `charity`, `thrift` | `charity_shop` | Consolidate variations |

**Proposed list:** `launderette`, `dry_cleaning`, `tailor`, `charity_shop`

---

### **Accommodation**
**Current:** 6 entries

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Hotel | `hotel` | `hotel` | Remove `hotel_chain` (venue type not relevant) |
| Hostel | `hostel` | `hostel` | KEEP |
| Guest Accom | `guest_house`, `bed_and_breakfast`, `b&b` | `guest_house`, `bed_and_breakfast` | Remove `b&b` (abbreviation) |

**Proposed list:** `hotel`, `hostel`, `guest_house`, `bed_and_breakfast`

---

### **Retail & Fashion**
**Current:** 15 entries

| Group | Current | Proposed | Reason |
|-------|---------|----------|--------|
| Footwear | `shoes`, `shoe_shop`, `footwear` | `footwear` | Consolidate variations |
| Cobbler | `cobbler` | `cobbler` | KEEP (distinct service) |
| Clothing | `clothing`, `apparel`, `fashion`, `boutique`, `dress_shop` | `clothing`, `boutique` | Remove `apparel`, `fashion` (too generic); keep `boutique` (specific) |
| Books | `bookshop`, `books`, `book_store` | `bookshop` | Consolidate variations |
| Stationery | `stationery` | `stationery` | KEEP |

**Proposed list:** `footwear`, `cobbler`, `clothing`, `boutique`, `bookshop`, `stationery`

---

## Summary Statistics

| Metric | Current | Proposed | Reduction |
|--------|---------|----------|-----------|
| **Total slugs** | 161 | 109 | **52 removed (32% reduction)** |
| **Duplicate pairs** | ~15 | 0 | — |
| **Spelling variations** | ~8 | 0 | — |

---

## Notes for Review

1. **Spelling standardisation:** Proposing British English throughout (e.g., `theatre`, `launderette`, `off_license`)
2. **Product vs. Venue:** Where items appear in data as both (e.g., `coffee` shop vs `coffee` product), kept the venue form
3. **Granularity:** Removed overly specific subcategories that duplicate their parent (e.g., `crossfit` → `gym`)
4. **Kept distinctions:** Where semantic difference exists (e.g., `tavern` vs `taproom`), both retained

---

## Action Items

- [ ] Review and edit this document
- [ ] Confirm final proposed lists
- [ ] Update `tag_auditor.html` CATEGORY_SLUGS constant
- [ ] Update any CSV/database references (check listings_rows-06.csv for used slugs)
