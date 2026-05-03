import re
from bs4 import BeautifulSoup

# HTML snippet from user
html = """<p class="_al _bj _cf _eu _af _jn"><span data-testid="rich-text" class="_jo _h9 _jp _be _bf _i8 _dj _jq"> • </span><span data-testid="rich-text" class="_jo _h9 _jp _be _bf _i8 _dj _jr">Desserts</span><span data-testid="rich-text" class="_jo _h9 _jp _be _bf _i8 _dj _jq"> • </span><span data-testid="rich-text" class="_jo _h9 _jp _be _bf _i8 _dj _jr">Coffee &amp; tea</span><span data-testid="rich-text" class="_jo _h9 _jp _be _bf _i8 _dj _jq"> • </span><span data-testid="rich-text" class="_jo _h9 _jp _be _bf _i8 _dj _jr">Ice Cream</span><span data-testid="rich-text" class="_jo _h9 _jp _be _bf _i8 _dj _jq"> • </span><span class="_js _af"><a class="_af _da _jt _be _bf _i8 _dj _jr" href="/gb/store/simple-pleasures/kyzQhh3aQq699O0q-Mn8nA?mod=storeInfo&amp;modctx=%257B%2522storeSlug%2522%253A%2522simple-pleasures%2522%252C%2522storeUuid%2522%253A%2522932cd086-1dda-42ae-bdf4-ed2af8c9fc9c%2522%252C%2522sectionUuid%2522%253A%2522%2522%257D&amp;ps=1">Info</a></span><p class="_al _bj _cf _eu _af _jn"><span data-testid="rich-text" class="_jo _h9 _jp _be _bf _i8 _dj _jq">Simple Pleasures, 71 Surbiton Road, London, England Kt1 2hg</span></p></p>"""

soup = BeautifulSoup(html, 'html.parser')
rich_text_spans = soup.find_all('span', {'data-testid': 'rich-text'})

print(f"Found {len(rich_text_spans)} spans with data-testid='rich-text':\n")

all_texts = []
for i, span in enumerate(rich_text_spans):
    text = span.get_text(strip=True)
    print(f"  [{i}] {repr(text)}")
    if text and text != '•':
        all_texts.append(text)

print(f"\nFiltered texts (no bullets): {all_texts}\n")

postcode_pattern = r'[a-zA-Z]{1,2}\d[a-zA-Z\d]?\s*\d[a-zA-Z]{2}'
address = None
categories = []

for text in all_texts:
    match = re.search(postcode_pattern, text)
    if match:
        print(f"✓ POSTCODE MATCH: '{match.group()}' in: {repr(text)}")
        address = text
    else:
        print(f"  Category candidate: {repr(text)}")
        categories.append(text)

print(f"\n✓ Address: {address}")
print(f"✓ Categories: {categories}")

food_keywords = ['dessert', 'coffee', 'tea', 'ice cream']
filtered_categories = [cat for cat in categories if any(keyword in cat.lower() for keyword in food_keywords)]
print(f"✓ Filtered categories: {filtered_categories}")
