from bs4 import BeautifulSoup
import requests

from scraper.objects import *

def extract_soup(url, header=0, preview=True):
    headers = headers_tuple[header]
    response = requests.get(url, headers=headers)
    status = response.status_code

    soup = BeautifulSoup(response.text, 'lxml')

    if preview==True:
        print(soup.prettify())

    return soup, status

def top_amazon_boxes(soup):
    boxes = soup.find_all('div', attrs={'class':"a-section a-spacing-none aok-relative"})

    return boxes