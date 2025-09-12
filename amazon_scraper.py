from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By

base_url = 'https://www.amazon.co.uk'

'''Method to configure Amazon url'''
def configure_amazon_url(search_item):
    start_url = base_url + '/s?k='
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    amazon_url = start_url + new_search
    return amazon_url

'''Using Selenium to produce an array of dictionaries, of products'''
def find_amazon_products(search_item):
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
                price = price_whole_element.text.strip() + price_frac_element.text.strip()

                products_list.append({
                    'name': product_name,
                    'url': product_url,
                    'price': price
                })
        except AttributeError:
            continue
    
    return products_list