from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

from operator import itemgetter

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

'''Method to configure Amazon url'''
def configure_amazon_url(search_item):
    start_url = 'https://www.amazon.co.uk/s?k='
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    amazon_url = start_url + new_search
    return amazon_url

'''Changing how the url looks based on how Scan queries for searches'''
def configure_scan_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    scan_url = 'https://www.scan.co.uk/search?q=' + new_search
    return scan_url

'''URL configurator based on Overclockers querying'''
def configure_oc_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '%2520')
    new_search = ''.join(new_search)
    oc_url = 'https://www.overclockers.co.uk/?query=' + new_search
    return oc_url

'''URL Configurator based on CCL's querying'''
def configure_ccl_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    ccl_url = 'https://www.cclonline.com/search/?q=' + new_search
    return ccl_url

'''Using Selenium to produce an array of dictionaries, of all_products'''
def find_amazon_products(search_item):
    base_url = 'www.amazon.co.uk'
    amazon_url = configure_amazon_url(search_item)
    options = webdriver.FirefoxOptions()
    # options.add_argument('--width=1920')
    # options.add_argument('--height=1080')
    options.add_argument("-headless")

    driver = webdriver.Firefox(options = options)
    driver.get(amazon_url)

    sleep(2)
    cookie_button = driver.find_element(By.ID,'sp-cc-rejectall-link')
    cookie_button.click()

    html = driver.page_source
    amazon_soup = BeautifulSoup(html, 'html.parser')
    listing_chunk = amazon_soup.find('div', class_='sg-col-4-of-4 sg-col-20-of-24 s-matching-dir sg-col-16-of-20 sg-col sg-col-12-of-12 sg-col-8-of-8 sg-col-12-of-16')
    listings = listing_chunk.find_all('div', class_='sg-col-4-of-4 sg-col-20-of-24 s-result-item s-asin sg-col-16-of-20 sg-col sg-col-12-of-12 s-widget-spacing-small sg-col-8-of-8 sg-col-12-of-16')

    sleep(0.5)
    products_list =[]
    for listing in listings:
        try:
            name_element_link = listing.find('a', class_ = 'a-link-normal s-line-clamp-2 s-line-clamp-3-for-col-12 s-link-style a-text-normal')
            name_element = name_element_link.find('span')
            price_whole_element = listing.find('span', class_='a-price-whole')
            price_frac_element = listing.find('span', class_='a-price-fraction')
            if name_element and price_whole_element:
                product_name = name_element.text.strip()
                product_url = base_url + name_element_link['href']
                price = '£' + price_whole_element.text.strip() + price_frac_element.text.strip()

                products_list.append({
                    'name': product_name,
                    'url': product_url,
                    'price': price
                })
        except AttributeError:
            continue
    
    return products_list

'''Returns an array of dictionaries of SCAN all_products'''
def find_scan_products(search_item):
    scan_response = requests.get(configure_scan_url(search_item), headers=headers)
    scan_soup = BeautifulSoup(scan_response.text, 'html.parser')
    
    product_containers = scan_soup.find_all('li', class_='product')
    
    base_url = 'www.scan.co.uk'
    products_list = []

    for container in product_containers:
        try:
            name_element = container.find('span', class_='description').find('a')
            price_element = container.find('span', class_='price')

            if name_element and price_element:
                product_name = name_element.text.strip()
                product_url = base_url + name_element['href']
                price = price_element.text.strip()

                products_list.append({
                    'name': product_name,
                    'url': product_url,
                    'price': price
                })
        except AttributeError:
            continue
    return products_list



'''Produces an array of dictionaries of all_products consisting product names, urls and price'''
def find_oc_products(search_item):
    
    options = webdriver.FirefoxOptions()
    # options.add_argument('--width=1920')
    # options.add_argument('--height=1080')
    options.add_argument("-headless")

    driver = webdriver.Firefox(options = options)
    driver.get(configure_oc_url(search_item))

    sleep(0.5)  # Sleep in order to wait for the cookie page to load
    cookie_button = driver.find_element(By.ID, "CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll")
    cookie_button.click()

    sleep(2)
    html = driver.page_source
    oc_soup = BeautifulSoup(html, 'html.parser')
    row_listings = oc_soup.find('div', class_='row row--listing js-hide--empty-search')
    cols = row_listings.find_all('div', class_='col')

    sleep(0.5)
    products_list = []
    base_url = 'www.overclockers.co.uk'
    for col in cols:
        try:
            name_element = col.find('h6', class_='h5 lh-1-4 mb-0 text-break').find('a')
            price_element = col.find('span', class_='price__amount')

            if name_element and price_element:
                product_name = name_element.text.strip()
                product_url = base_url + name_element['href']
                price = price_element.text.strip()

                products_list.append({
                    'name': product_name,
                    'url': product_url,
                    'price': price
                })
        except AttributeError:
            continue
    
    return products_list

'''Returns an array of dictionaries of CCL all_products'''
def find_ccl_products(search_item):

    base_url = 'www.cclonline.com'

    options = webdriver.FirefoxOptions()
    # options.add_argument('--width=1920')
    # options.add_argument('--height=1080')
    options.add_argument("-headless")

    driver = webdriver.Firefox(options = options)
    driver.get(configure_ccl_url(search_item))

    sleep(0.5)
    cookie_button = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    cookie_button.click()
    
    sleep(0.5)
    html = driver.page_source
    ccl_soup = BeautifulSoup(html, 'html.parser')
    listing_chunk = ccl_soup.find('div', class_='productListContainer pt-3 row px-2 px-xs-3 px-sm-3 px-md-0 mx-md-n2')
    listings = listing_chunk.find_all('div', class_='productListOverlayWrapper position-relative col-12 col-xs-6 col-sm-6 col-md-4 px-2 px-xs-0 px-sm-2')

    products_list = []
    for listing in listings:
        try:
            name_element = listing.find('h3', class_='product-name text-center').find('a')
            price_element = listing.find('p', class_='order-xs-2')
            if name_element and price_element:
                product_name = name_element.text
                product_url = base_url + name_element['href']
                price = price_element.text.strip().split()[0]
                products_list.append({
                    'name': product_name,
                    'url': product_url,
                    'price': price
                })
        except AttributeError:
            continue
    
    return products_list

def get_all_products(search_item):
    amazon_products = find_amazon_products(search_item)
    scan_products = find_scan_products(search_item)
    oc_products = find_oc_products(search_item)
    ccl_prodcuts = find_ccl_products(search_item)

    all_products = amazon_products + scan_products + oc_products + ccl_prodcuts
    cleaned_products = []
    for x in all_products:
        p = (x['price'].replace('£', '').replace(',', ''))
        x['price'] = float(p)
        cleaned_products.append(x)

    sorted_products = sorted(cleaned_products, key=itemgetter('price'))
    return sorted_products    

'''Print test statements'''