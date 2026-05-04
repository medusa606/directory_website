import os
import xml.etree.ElementTree as ET
import csv
import argparse
from urllib.parse import urlparse

OUTPUT_CSV = 'deliveroo.csv'
SITEMAP_FILE = 'bookings/deliveroo-sitemap_menu-8.xml'

def parse_sitemap_xml(path):
    """Parse sitemap XML and extract all URLs."""
    try:
        tree = ET.parse(path)
        root = tree.getroot()
        urls = []
        for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
            url = url_elem.text
            if url:
                urls.append(url)
        return urls
    except Exception as e:
        print(f"✗ Error parsing {path}: {e}")
        return []

def extract_deliveroo_info(url):
    """
    Extract city, area, and name from Deliveroo URL.
    URL format: https://deliveroo.co.uk/menu/bristol/st-judes-and-easton/lucky-chef-chinese-takeaway-bristol
    """
    try:
        parsed = urlparse(url)
        parts = parsed.path.strip('/').split('/')
        
        # parts = [menu, city, area, full-name-with-city]
        if len(parts) < 4 or parts[0] != 'menu':
            return None, None, None
        
        city = parts[1]
        area = parts[2]
        name = parts[3]  # Keep the full name
        
        return city, area, name
    except Exception as e:
        print(f"  ✗ Error parsing URL {url}: {e}")
        return None, None, None

def main():
    parser = argparse.ArgumentParser(description='Deliveroo Bristol restaurants scraper')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of listings to process (for testing)')
    args = parser.parse_args()
    
    print("=" * 60)
    print("DELIVEROO BRISTOL RESTAURANTS SCRAPER")
    if args.limit:
        print(f"LIMIT: {args.limit} listings")
    print("=" * 60)
    
    # Check if sitemap file exists
    if not os.path.exists(SITEMAP_FILE):
        print(f"✗ Sitemap file not found: {SITEMAP_FILE}")
        return
    
    # Load existing URLs to skip duplicates
    existing_urls = set()
    existing_rows = []
    if os.path.exists(OUTPUT_CSV):
        print(f"\n[INIT] Loading existing CSV: {OUTPUT_CSV}")
        try:
            with open(OUTPUT_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    existing_rows.append(row)
                    existing_urls.add(row['url'])
            print(f"✓ Found {len(existing_urls)} existing URLs")
        except Exception as e:
            print(f"✗ Error loading CSV: {e}")
    
    # Step 1: Parse sitemap
    print(f"\n[STEP 1] Parsing sitemap: {SITEMAP_FILE}")
    all_urls = parse_sitemap_xml(SITEMAP_FILE)
    print(f"Found {len(all_urls)} total URLs in sitemap")
    
    # Step 2: Filter for Bristol restaurants (containing 'menu/bristol')
    print(f"\n[STEP 2] Filtering for Bristol restaurants...")
    bristol_urls = [url for url in all_urls if '/menu/bristol/' in url]
    print(f"Found {len(bristol_urls)} Bristol restaurants")
    
    # Step 3: Filter out already processed URLs
    new_urls = [url for url in bristol_urls if url not in existing_urls]
    print(f"Skipping {len(existing_urls)} already processed URLs")
    print(f"Processing {len(new_urls)} new URLs")
    
    # Apply limit if specified
    if args.limit:
        new_urls = new_urls[:args.limit]
        print(f"Limited to {len(new_urls)} listings for testing")
    
    # Step 3: Extract info and build rows
    print(f"\n[STEP 3] Extracting restaurant details...")
    rows = existing_rows.copy()
    
    for i, url in enumerate(new_urls, 1):
        city, area, name = extract_deliveroo_info(url)
        
        if not name:
            print(f"[{i}/{len(new_urls)}] ✗ Could not parse: {url}")
            continue
        
        rows.append({
            'service': 'deliveroo',
            'name': name,
            'city': city,
            'area': area,
            'url': url
        })
        print(f"[{i}/{len(new_urls)}] {name} ({area})")
        
        # Save every 10 entries
        if i % 10 == 0:
            print(f"  💾 Saving checkpoint at {i} entries...")
            with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['service', 'name', 'city', 'area', 'url'])
                writer.writeheader()
                for row in rows:
                    writer.writerow(row)
            print(f"  ✓ Saved {len(rows)} total rows")
    
    # Final save
    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['service', 'name', 'city', 'area', 'url'])
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    
    print(f"\n✓ Final write: {len(rows)} total rows to {OUTPUT_CSV}")
    print("=" * 60)

if __name__ == '__main__':
    main()
