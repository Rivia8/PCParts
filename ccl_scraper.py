from time import sleep

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By



'''URL Configurator based on CCL's querying'''
def configure_ccl_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    ccl_url = 'https://www.cclonline.com/search/?q=' + new_search
    return ccl_url

'''Returns an array of dictionaries of CCL products'''
def find_ccl_products(search_item):

    base_url = 'https://www.cclonline.com'

    options = webdriver.FirefoxOptions()
    options.add_argument('--width=1920')
    options.add_argument('--height=1080')
    # options.add_argument("-headless")

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