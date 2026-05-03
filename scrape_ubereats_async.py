import os
import gzip
import xml.etree.ElementTree as ET
import csv
import re
import requests
import argparse
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from pathlib import Path
from playwright.async_api import async_playwright

SITEMAP_LIST = 'bookings/uber-eats-site-map-stores.txt'
OUTPUT_CSV = 'bookings.csv'
BOOKINGS_DIR = 'bookings'
UK_SITEMAP_OUTPUT = 'bookings/uber-uk-sitemap.xml'

# Uber Eats sitemap URLs to download
UBER_EATS_SITEMAPS = [
    'https://www.ubereats.com/sitemap-store-771af823-025.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-024.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-023.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-022.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-021.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-020.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-019.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-018.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-017.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-016.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-015.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-014.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-013.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-012.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-011.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-010.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-009.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-008.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-007.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-006.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-005.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-004.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-003.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-002.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-001.xml.gz',
    'https://www.ubereats.com/sitemap-store-771af823-000.xml.gz',
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (compatible; DirectoryWebsiteBot/1.0)'
}

# Global lock for thread-safe CSV writes
csv_lock = asyncio.Lock()

def parse_sitemap_xml(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        url = url_elem.text
        if '/gb/' in url:
            yield url

async def extract_ubereats_info(url, page):
    """Extract address and categories using Playwright for JavaScript rendering."""
    try:
        # Load with a more lenient wait condition
        response = await page.goto(url, wait_until='domcontentloaded', timeout=15000)
        
        # Give it a moment to render
        await page.wait_for_timeout(2000)
        
        # Check for closed/error messages
        error_count = await page.locator('text="Restaurant closed"').count()
        if error_count > 0:
            return None, None
        
        # Get page content
        content = await page.content()
        
        # Check if we got anything useful
        if 'rich-text' not in content:
            return None, None
        
        soup = BeautifulSoup(content, 'html.parser')
        
        # Find ALL spans with data-testid="rich-text"
        rich_text_spans = soup.find_all('span', {'data-testid': 'rich-text'})
        
        # Collect all text from rich-text spans
        all_texts = []
        for span in rich_text_spans:
            text = span.get_text(strip=True)
            if text and text != '•':
                all_texts.append(text)
        
        if not all_texts:
            return None, None
        
        # UK postcode pattern: case-insensitive, flexible spacing
        postcode_pattern = r'[a-zA-Z]{1,2}\d[a-zA-Z\d]?\s*\d[a-zA-Z]{2}'
        
        address = None
        categories = []
        
        # Address keywords to validate real addresses
        address_keywords = ['road', 'street', 'lane', 'avenue', 'drive', 'close', 'court', 'park', 'terrace', 'rd', 'st', 'london', 'bristol', 'manchester', 'birmingham', 'leeds', 'glasgow', 'edinburgh', 'cardiff', 'england', 'scotland', 'wales', 'northern ireland', 'surbiton', 'derby', 'telford']
        
        for text in all_texts:
            # Check if this text contains a postcode AND address keywords
            match = re.search(postcode_pattern, text)
            if match:
                # Validate it's a real address: must have postcode + address keyword + reasonable length
                has_address_keyword = any(keyword in text.lower() for keyword in address_keywords)
                is_long_enough = len(text) > 15
                
                if has_address_keyword and is_long_enough and not address:
                    # This is the address
                    address = text.rstrip(', ').replace('United Kingdom, ', '').replace('united kingdom, ', '').rstrip(', ')
                    continue
            
            # Everything else is a potential category
            if text not in categories:
                categories.append(text)
        
        # Filter categories by food keywords
        food_keywords = ['dessert', 'coffee', 'tea', 'ice cream', 'pizza', 'burger', 'sushi', 'sandwich', 'breakfast', 'bakery', 'drink', 'salad', 'chicken', 'chinese', 'indian', 'thai', 'mexican', 'vegan', 'vegetarian', 'pasta', 'steak', 'fish', 'curry', 'ramen', 'tapas', 'french', 'italian', 'japanese', 'korean', 'vietnamese', 'middle eastern', 'mediterranean', 'brunch', 'lunch', 'dinner', 'kebab', 'donuts', 'wings', 'noodles', 'rice', 'soup', 'grill', 'bbq', 'seafood', 'fried chicken', 'tacos', 'burritos', 'fried', 'gyros', 'wraps', 'halal', 'kosher', 'gluten-free', 'smoothie', 'juice', 'acai', 'bubble tea']
        filtered_categories = [cat for cat in categories if any(keyword in cat.lower() for keyword in food_keywords)]
        
        return address, ' • '.join(filtered_categories) if filtered_categories else None
    except Exception as e:
        return None, None

async def fetch_restaurant(url, page_queue, index, total):
    """Fetch one restaurant, handle concurrency safely."""
    # Borrow a page from the pool
    page = await page_queue.get()
    try:
        # Extract info
        address, categories = await extract_ubereats_info(url, page)
        
        # Parse URL for service and name
        parsed = urlparse(url)
        parts = parsed.path.strip('/').split('/')
        name = parts[2] if len(parts) > 2 else ''
        
        if address is None:
            address = 'closed'
        
        row = {
            'service': 'uber_eats',
            'name': name,
            'url': url,
            'address': address,
            'categories': categories or ''
        }
        
        print(f"[{index}/{total}] {name}: {address} [{categories}]")
        return row
    except Exception as e:
        print(f"[{index}/{total}] ✗ Error: {str(e)[:60]}")
        return None
    finally:
        # Return page to pool
        await page_queue.put(page)

async def save_checkpoint(rows, label=""):
    """Save checkpoint to CSV with lock protection."""
    async with csv_lock:
        with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['service', 'name', 'url', 'address', 'categories'])
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
    print(f"  💾 {label} Saved {len(rows)} total rows to {OUTPUT_CSV}")

def download_sitemaps():
    """Download all Uber Eats sitemap files and extract them."""
    Path(BOOKINGS_DIR).mkdir(exist_ok=True)
    local_paths = []
    
    for url in UBER_EATS_SITEMAPS:
        filename = os.path.basename(url)
        local_path = os.path.join(BOOKINGS_DIR, filename)
        
        if os.path.exists(local_path):
            print(f"✓ {filename} already exists, skipping download")
        else:
            print(f"⬇ Downloading {filename}...")
            try:
                r = requests.get(url, headers=HEADERS, timeout=30)
                r.raise_for_status()
                with open(local_path, 'wb') as f:
                    f.write(r.content)
                print(f"✓ Downloaded {filename}")
            except Exception as e:
                print(f"✗ Failed to download {filename}: {e}")
                continue
        
        local_paths.append(local_path)
    
    return local_paths

def collect_uk_urls(sitemap_paths):
    """Parse all sitemaps and collect UK URLs (/gb/ slug)."""
    uk_urls = []
    
    for path in sitemap_paths:
        print(f"Parsing {os.path.basename(path)}...")
        try:
            if path.endswith('.gz'):
                with gzip.open(path, 'rt', encoding='utf-8') as f:
                    tree = ET.parse(f)
            else:
                tree = ET.parse(path)
            
            root = tree.getroot()
            for url_elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
                url = url_elem.text
                if url and '/gb/' in url:
                    uk_urls.append(url)
        except Exception as e:
            print(f"✗ Error parsing {path}: {e}")
            continue
    
    return uk_urls

def create_uk_sitemap(uk_urls):
    """Create a consolidated sitemap with only UK URLs."""
    print(f"\nCreating UK sitemap with {len(uk_urls)} entries...")
    
    # Create XML structure
    root = ET.Element('urlset')
    root.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
    
    for url in sorted(set(uk_urls)):  # Remove duplicates
        url_elem = ET.SubElement(root, 'url')
        loc = ET.SubElement(url_elem, 'loc')
        loc.text = url
    
    # Write to file
    tree = ET.ElementTree(root)
    tree.write(UK_SITEMAP_OUTPUT, encoding='utf-8', xml_declaration=True)
    print(f"✓ Created {UK_SITEMAP_OUTPUT} with {len(set(uk_urls))} unique UK listings")

async def main():
    parser = argparse.ArgumentParser(description='Uber Eats UK sitemap scraper (ASYNC)')
    parser.add_argument('--limit', type=int, default=None, help='Limit number of listings to process (for testing)')
    parser.add_argument('--concurrency', type=int, default=5, help='Number of concurrent page fetches (default: 5)')
    args = parser.parse_args()
    
    print("=" * 60)
    print("UBER EATS UK SITEMAP & LISTINGS SCRAPER (ASYNC)")
    if args.limit:
        print(f"LIMIT: {args.limit} listings")
    print(f"CONCURRENCY: {args.concurrency} pages")
    print("=" * 60)
    
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
    
    # Step 1: Download all sitemaps
    print("\n[STEP 1] Downloading sitemaps...")
    sitemap_paths = download_sitemaps()
    
    # Step 2: Collect UK URLs and create consolidated sitemap
    print("\n[STEP 2] Collecting UK URLs...")
    uk_urls = collect_uk_urls(sitemap_paths)
    
    # Apply limit if specified
    if args.limit:
        uk_urls = uk_urls[:args.limit]
        print(f"Limited to {len(uk_urls)} URLs for testing")
    
    # Filter out URLs already processed
    new_urls = [url for url in uk_urls if url not in existing_urls]
    print(f"Skipping {len(existing_urls)} already processed URLs")
    print(f"Processing {len(new_urls)} new URLs")
    
    if new_urls:
        print("\n[STEP 3] Creating consolidated UK sitemap...")
        create_uk_sitemap(new_urls)
    else:
        print("⚠ No new URLs to process")
        return
    
    # Step 4: Extract store details from UK listings (ASYNC)
    print("\n[STEP 4] Extracting store details (ASYNC)...")
    rows = existing_rows.copy()
    total_urls = len(new_urls)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            extra_http_headers={
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-GB,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Pragma': 'no-cache'
            }
        )
        
        # Create page pool
        page_queue = asyncio.Queue(maxsize=args.concurrency)
        for _ in range(args.concurrency):
            page = await context.new_page()
            await page_queue.put(page)
        
        # Create fetch tasks for all URLs
        fetch_tasks = []
        for i, url in enumerate(new_urls, 1):
            task = asyncio.create_task(fetch_restaurant(url, page_queue, i, total_urls))
            fetch_tasks.append(task)
        
        # Process results as they complete
        checkpoint_counter = 0
        for i, task in enumerate(asyncio.as_completed(fetch_tasks), 1):
            result = await task
            if result:
                rows.append(result)
                checkpoint_counter += 1
                
                # Save every 10 entries
                if checkpoint_counter % 10 == 0:
                    await save_checkpoint(rows, f"Checkpoint {checkpoint_counter//10}")
        
        # Close browser
        await context.close()
        await browser.close()
    
    # Final save
    await save_checkpoint(rows, "Final write")
    print("=" * 60)

if __name__ == '__main__':
    asyncio.run(main())
