import requests
from bs4 import BeautifulSoup
import pandas as pd

def scrape_product_listings(url, pages=20):
    product_data = []
    
    for page in range(1, pages + 1):
        page_url = f"{url}&page={page}"
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Scraping the product details
        product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for container in product_containers:
            product_url = container.find('a', {'class': 'a-link-normal'})['href']
            product_name = container.find('span', {'class': 'a-size-medium'}).text.strip()
            
            # Check if the price element exists before accessing its text
            price_elem = container.find('span', {'class': 'a-offscreen'})
            product_price = price_elem.text.strip() if price_elem else 'Price not available'
            
            rating = container.find('span', {'class': 'a-icon-alt'})
            product_rating = rating.text.split()[0] if rating else 'Not rated'
            
            reviews = container.find('span', {'class': 'a-size-base'})
            product_reviews = reviews.text if reviews else '0'
            
            product_data.append([product_url, product_name, product_price, product_rating, product_reviews])
            
    return product_data

def scrape_product_details(product_urls):
    product_details = []

    for url in product_urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Scraping the product details
        # Add your code here to extract ASIN, product description, manufacturer, etc.
        # Replace 'ASIN', 'Product Description', and 'Manufacturer' with the actual tags/classes you want to scrape
        
        product_asin = ''
        product_description = ''
        product_manufacturer = ''
        
        product_details.append([url, product_description, product_asin, product_description, product_manufacturer])
        
    return product_details

def save_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews'])
    df.to_csv(filename, index=False)

def save_details_to_csv(data, filename):
    df = pd.DataFrame(data, columns=['Product URL', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])
    df.to_csv(filename, index=False)

if __name__ == "__main__":
    base_url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_1"
    
    # Part 1: Scraping Product Listings
    product_data = scrape_product_listings(base_url, pages=20)
    save_to_csv(product_data, "product_listings.csv")
    
    # Extracting product URLs from the scraped data
    product_urls = [item[0] for item in product_data]

    # Part 2: Scraping Individual Product Pages
    product_details = scrape_product_details(product_urls)
    save_details_to_csv(product_details, "product_details.csv")
