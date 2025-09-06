from bs4 import BeautifulSoup
import requests

import time
import random

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

'''Changing how the url looks based on how Scan queries for searches'''
def configure_scan_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '+')
    new_search = ''.join(new_search)
    scan_url = 'https://www.scan.co.uk/search?q=' + new_search
    return scan_url

'''Produces a dictionary of products with product names'''
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


    


search_item = 'rtx 5080'
print(find_scan_products(search_item))