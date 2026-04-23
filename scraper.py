# Web scraper to extract product information from atlet.az
# This script visits all product category pages AND individual product pages
# to build a detailed product database with brand, description, etc.

# Import required libraries
import requests  # For making HTTP requests to websites
from bs4 import BeautifulSoup  # For parsing HTML and extracting data
import json  # For saving data in JSON format
import time  # For adding delays between requests

# ============================================
# CONFIGURATION - List of all category URLs
# ============================================
# These are all the product categories on atlet.az
# We'll visit each one and extract all products
CATEGORY_URLS = {
    'protein': 'https://atlet.az/shop/protein',
    'kreatin': 'https://atlet.az/shop/kreatin',
    'qeyner': 'https://atlet.az/shop/qeyner',
    'vitaminler': 'https://atlet.az/shop/vitaminler',
    'amino': 'https://atlet.az/shop/amino',
    'energetik': 'https://atlet.az/shop/energetik',
    'piyyandiricilar': 'https://atlet.az/shop/piyyandiricilar',
    'fitnes-qida': 'https://atlet.az/shop/fitnes-qida',
    'aksesuarlar': 'https://atlet.az/shop/aksesuarlar'
}

# Set up request headers to mimic a real browser
# Some websites block requests that don't look like they come from a browser
# The User-Agent header tells the website we're using a normal browser
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# ============================================
# FUNCTION: Scrape a single category page
# ============================================
def scrape_category(category_name, category_url):
    """
    Scrapes all products from a single category page.
    Returns basic product info: name, price, category, url.
    We'll add brand and description later by visiting each product page.
    """
    print(f"\n[*] Scraping category: {category_name}")
    print(f"   URL: {category_url}")

    # List to store all products from this category
    products = []

    try:
        # Make an HTTP GET request to the category page
        # This downloads the HTML of the page
        # timeout=10 means we'll wait max 10 seconds for a response
        response = requests.get(category_url, headers=HEADERS, timeout=10)

        # Check if the request was successful
        # Status code 200 means success
        if response.status_code != 200:
            print(f"   [ERROR] Got status code {response.status_code}")
            return products

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all product links on the page
        # Based on inspection: each product is an <a> tag containing an <h3> and price with manat
        all_links = soup.find_all('a', href=True)

        # Filter to only product links (those that contain both h3 and manat symbol)
        product_items = []
        for link in all_links:
            if link.find('h3') and '\u20bc' in link.get_text():
                product_items.append(link)

        print(f"   Found {len(product_items)} products")

        # Loop through each product link and extract basic information
        for item in product_items:
            try:
                # Extract product name from <h3> tag
                name_element = item.find('h3')
                product_name = name_element.get_text(strip=True) if name_element else "Unknown Product"

                # Extract product price (text containing manat symbol)
                full_text = item.get_text()
                price_parts = full_text.split()
                product_price = "Price not found"
                for part in price_parts:
                    if '\u20bc' in part:
                        product_price = part.strip()
                        break

                # Extract product URL and make it absolute
                product_url = item['href']
                if not product_url.startswith('http'):
                    product_url = 'https://atlet.az/' + product_url.lstrip('/')

                # Create a dictionary with basic product information
                # Brand and description will be added later
                product_data = {
                    'name': product_name,
                    'price': product_price,
                    'category': category_name,
                    'url': product_url,
                    'brand': '',          # Will be filled by scrape_product_details()
                    'description': ''     # Will be filled by scrape_product_details()
                }

                products.append(product_data)

            except Exception as e:
                print(f"   [WARNING] Error extracting product: {e}")
                continue

        print(f"   [SUCCESS] Scraped {len(products)} products from {category_name}")

    except Exception as e:
        print(f"   [ERROR] Error scraping category {category_name}: {e}")

    return products


# ============================================
# FUNCTION: Scrape details from individual product page
# ============================================
def scrape_product_details(product):
    """
    Visits a single product's detail page and extracts:
    - Brand name (from <a> tag with href containing 'brend/')
    - Description (from <p> tags in the page content)

    Parameters:
    - product: a dictionary with at least a 'url' key

    Returns:
    - Updated product dictionary with 'brand' and 'description' filled in
    """
    try:
        # Make an HTTP GET request to the individual product page
        response = requests.get(product['url'], headers=HEADERS, timeout=10)

        if response.status_code != 200:
            return product

        # Parse the product detail page HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # ---- EXTRACT BRAND ----
        # The brand link has this structure:
        #   <a class="product-brand-box" href="brend/body-attack">
        #     <span class="title">Body Attack</span>
        #     <p class="info">100% orijinal...</p>
        #   </a>
        # We want ONLY the <span class="title"> text, not the whole link text
        brand_link = soup.find('a', href=lambda h: h and 'brend/' in h)
        if brand_link:
            # Look for the <span class="title"> inside the brand link
            # This contains ONLY the brand name like "Body Attack" or "Nutrex"
            brand_title = brand_link.find('span', class_='title')
            if brand_title:
                product['brand'] = brand_title.get_text(strip=True)
            else:
                # Fallback: extract brand from the URL path
                # "brend/body-attack" -> "body-attack" -> "Body Attack"
                brand_slug = brand_link['href'].split('brend/')[-1]
                product['brand'] = brand_slug.replace('-', ' ').title()

        # ---- EXTRACT DESCRIPTION ----
        # The actual product description is inside a div with id="Disclosure"
        # This is the "Etrafli" (Details) tab content on the product page
        # It contains <p> tags with the real description, nutritional info, etc.
        disclosure = soup.find(id='Disclosure')
        if disclosure:
            # Get all <p> tags inside the Disclosure section
            paragraphs = disclosure.find_all('p')
            description_parts = []

            for p in paragraphs:
                # Get clean text from each paragraph
                text = p.get_text(strip=True)
                # Only include non-empty paragraphs
                if text:
                    description_parts.append(text)

            # Join all paragraphs into one description string
            # This gives us the full product description with nutritional info
            if description_parts:
                product['description'] = ' | '.join(description_parts)

    except Exception as e:
        # If we can't reach the product page, keep existing data
        # The product still has name, price, category, url from the category page
        print(f"   [WARNING] Could not get details for {product['name']}: {e}")

    return product


# ============================================
# MAIN SCRAPING FUNCTION
# ============================================
def scrape_all_categories():
    """
    Scrapes all product categories, then visits each product page for details.
    Saves everything to products.json
    """
    print("=" * 60)
    print("ATLET.AZ Product Scraper (Enhanced)")
    print("=" * 60)
    print(f"Scraping {len(CATEGORY_URLS)} categories...")

    # ---- PHASE 1: Scrape category pages for basic product info ----
    all_products = []

    for category_name, category_url in CATEGORY_URLS.items():
        category_products = scrape_category(category_name, category_url)
        all_products.extend(category_products)

        # Be respectful - wait 1 second between category pages
        print("   [WAIT] Waiting 1 second before next category...")
        time.sleep(1)

    print(f"\n{'=' * 60}")
    print(f"Phase 1 complete: {len(all_products)} products found")
    print(f"{'=' * 60}")

    # ---- PHASE 2: Visit each product page for brand and description ----
    print(f"\nPhase 2: Visiting {len(all_products)} product pages for details...")
    print("This will take about 2 minutes. Please wait...\n")

    for i, product in enumerate(all_products):
        # Show progress so the user knows it's working
        # Example: "[15/96] Scraping: Clear Iso Whey..."
        print(f"   [{i+1}/{len(all_products)}] {product['name']}...", end=" ")

        # Visit the product's detail page and extract brand + description
        scrape_product_details(product)

        # Show what we found
        brand_status = product['brand'] if product['brand'] else "no brand"
        desc_status = "has description" if product['description'] else "no description"
        print(f"({brand_status}, {desc_status})")

        # Be respectful - wait 1 second between product page requests
        time.sleep(1)

    # ============================================
    # SAVE TO JSON FILE
    # ============================================
    print(f"\n{'=' * 60}")
    print(f"Total products scraped: {len(all_products)}")
    print("Saving to products.json...")

    # Open (or create) products.json file for writing
    # encoding='utf-8' ensures Azerbaijani characters are saved correctly
    with open('products.json', 'w', encoding='utf-8') as f:
        # Convert our Python list to JSON format and write to file
        # indent=2 makes the JSON file nicely formatted and readable
        # ensure_ascii=False allows Azerbaijani characters to be saved properly
        json.dump(all_products, f, indent=2, ensure_ascii=False)

    print("[SUCCESS] Done! Products saved to products.json")
    print("=" * 60)

    # Print some statistics
    print("\nStatistics:")
    category_counts = {}
    brands_found = 0
    descriptions_found = 0

    for product in all_products:
        cat = product['category']
        category_counts[cat] = category_counts.get(cat, 0) + 1
        if product['brand']:
            brands_found += 1
        if product['description']:
            descriptions_found += 1

    for category, count in category_counts.items():
        print(f"   {category}: {count} products")

    print(f"\n   Brands found: {brands_found}/{len(all_products)}")
    print(f"   Descriptions found: {descriptions_found}/{len(all_products)}")


# ============================================
# RUN THE SCRAPER
# ============================================
# This only runs if we execute this file directly (not when importing it)
if __name__ == "__main__":
    scrape_all_categories()
