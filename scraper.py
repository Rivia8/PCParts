from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common import TimeoutException
from bs4 import BeautifulSoup
import requests
from operator import itemgetter

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

'''Amazon url configurator'''
def configure_amazon_url(search_item):
    start_url = 'https://www.amazon.co.uk/s?k='
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    amazon_url = start_url + new_search
    return amazon_url

'''eBay url configurator'''
def configure_eBay_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    scan_url = 'https://www.ebay.co.uk/sch/i.html?_nkw=' + new_search
    return scan_url
    
'''Scan url configurator'''
def configure_scan_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    scan_url = 'https://www.scan.co.uk/search?q=' + new_search
    return scan_url

'''Overclockers url configurator'''
def configure_oc_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '%2520')
    new_search = ''.join(new_search)
    oc_url = 'https://www.overclockers.co.uk/?query=' + new_search
    return oc_url

'''CCL url configurator '''
def configure_ccl_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    ccl_url = 'https://www.cclonline.com/search/?q=' + new_search
    return ccl_url

'''Returns an array of dictionaries of amazon products'''
def find_amazon_products(search_item):
    base_url = 'www.amazon.co.uk'
    amazon_url = configure_amazon_url(search_item)
    options = webdriver.FirefoxOptions()
    # options.add_argument('--width=1920')
    # options.add_argument('--height=1080')
    options.add_argument("-headless")

    driver = webdriver.Firefox(options = options)
    driver.get(amazon_url)

    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.element_to_be_clickable((By.ID,'sp-cc-rejectall-link'))).click()

        html = driver.page_source
        amazon_soup = BeautifulSoup(html, 'html.parser')
        listing_chunk = amazon_soup.find('div', class_='sg-col-4-of-4 sg-col-20-of-24 s-matching-dir sg-col-16-of-20 sg-col sg-col-12-of-12 sg-col-8-of-8 sg-col-12-of-16')
        listings = listing_chunk.find_all('div', class_='sg-col-4-of-4 sg-col-20-of-24 s-result-item s-asin sg-col-16-of-20 sg-col sg-col-12-of-12 s-widget-spacing-small sg-col-8-of-8 sg-col-12-of-16')

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
    except TimeoutException:
        print("The webpage did not load in time")
    
    return products_list

def find_eBay_products(search_item):
    ebay_url = configure_eBay_url(search_item)
    options = webdriver.FirefoxOptions()
    # options.add_argument('--width=1920')
    # options.add_argument('--height=1080')
    options.add_argument("-headless")
    driver = webdriver.Firefox(options = options)
    driver.get(ebay_url)

    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.element_to_be_clickable((By.ID,'gdpr-banner-decline'))).click()

        wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'srp-controls__count-heading')))
        html = driver.page_source
        eBay_soup = BeautifulSoup(html, 'html.parser')
        listing_chunk = eBay_soup.find('div', class_='srp-river-main')
        listings = listing_chunk.find_all('div', class_='su-card-container__content')
        products_list = []
        for listing in listings:
            try:
                name_element = listing.find('a', class_='su-link')
                price_element = listing.find('div', class_='s-card__attribute-row').find('span', class_='su-styled-text primary bold large-1 s-card__price')
                if name_element and price_element:
                    product_name = name_element.text.strip()
                    product_url = name_element['href']
                    price = price_element.text.strip()

                    products_list.append({
                        'name': product_name,
                        'url': product_url,
                        'price': price
                    })
            except AttributeError:
                continue
    except TimeoutException:
        print("The webpage did not load in time")
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

    try:
        wait = WebDriverWait(driver, 5)
        wait.until(EC.element_to_be_clickable((By.ID,'CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll'))).click()
    
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ais-Stats')))
        html = driver.page_source
        oc_soup = BeautifulSoup(html, 'html.parser')
        row_listings = oc_soup.find('div', class_='row row--listing js-hide--empty-search')
        cols = row_listings.find_all('div', class_='col')

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
    except TimeoutException:
        print("The webpage did not load in time")

    return products_list

'''Returns an array of dictionaries of CCL all_products'''
def find_ccl_products(search_item):

    base_url = 'www.cclonline.com'

    options = webdriver.FirefoxOptions()
    # options.add_argument('--width=1920')
    # options.add_argument('--height=1080')
    options.add_argument("-headless")

    try:
        driver = webdriver.Firefox(options = options)
        driver.get(configure_ccl_url(search_item))

        wait = WebDriverWait(driver, 5)
        wait.until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler'))).click()

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
    except TimeoutException:
        print('The webpage did not load in time')
    return products_list

def get_all_products(search_item, is_used):
    '''
    final function to combine and sort all products

    param search_item: string that is used as a query for all products
    param is_used: boolean that is true if the checkbox is ticked to included used items
    return: returns an array of dictionaries of products
    '''
    amazon_products = find_amazon_products(search_item)
    scan_products = find_scan_products(search_item)
    oc_products = find_oc_products(search_item)
    ccl_prodcuts = find_ccl_products(search_item)
    eBay_products = []

    if is_used:
        eBay_products = find_eBay_products(search_item)

    all_products =  amazon_products + eBay_products + scan_products + oc_products + ccl_prodcuts
    cleaned_products = []
    for x in all_products:
        p = (x['price'].replace('£', '').replace('$', '').replace(',', ''))
        x['price'] = float(p)
        cleaned_products.append(x)

    sorted_products = sorted(cleaned_products, key=itemgetter('price'))
    return sorted_products
    # search_item = search_item
    # temp = [{'name': 'gpu1', 'url': 'gpu.com', 'price': '458'}]
    # return temp

'''Print test statements'''
# print(find_eBay_products('rtx 5080'))