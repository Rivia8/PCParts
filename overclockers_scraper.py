from bs4 import BeautifulSoup
import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'
}

'''URL configurator based on OverClockers querying'''
def configure_oc_url(search_item):
    search = search_item.split()
    new_search = []
    for x in search:
        new_search.append(x + '%2520')
    new_search = ''.join(new_search)
    oc_url = 'https://www.overclockers.co.uk/?query=' + new_search
    return oc_url

print(configure_oc_url('rtx 5080'))