from bs4 import BeautifulSoup
import requests

import time
import random


def configure_scan_url():
    temp = "rx 9070xt"
    search = temp.split()
    new_search = []
    for x in search:
        new_search.append(x + "+")
    new_search = ''.join(new_search)
    scan_url = "https://www.scan.co.uk/search?q=" + new_search
    return scan_url


def find_scan_prices():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
    }
    scan_response = requests.get(configure_scan_url(), headers=headers)
    scan_soup = BeautifulSoup(scan_response.text, "html.parser")
    price_tags = scan_soup.find_all('span', class_="price")
    prices = []
    for tag in price_tags:
        raw_text = tag.text
        clean_text = raw_text.replace('£', '')
        prices.append(clean_text)
    cleaned_prices = []
    for x in prices:
        try:
            price = float(x)
            cleaned_prices.append(price)
        except:
            pass
    print(cleaned_prices)
        
find_scan_prices()