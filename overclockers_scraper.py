from time import sleep

from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By

'''URL configurator based on Overclockers querying'''
def configure_oc_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '%2520')
    new_search = ''.join(new_search)
    oc_url = 'https://www.overclockers.co.uk/?query=' + new_search
    return oc_url

'''Produces an array of dictionaries of products consisting product names, urls and price'''
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
    base_url = 'https://www.overclockers.co.uk'
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