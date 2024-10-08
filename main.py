from scraper.scraper import House
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
import requests
from requests import Session
import asyncio

def scrape_list_of_houses(url):
    # Set up custom headers
    headers = requests.utils.default_headers()
    headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    })
    session = Session()
    # Send GET request
    response = session.get(url, headers=headers)

    # Parse the page content
    soup = BeautifulSoup(response.content, "html.parser")

    # Scrape the property links
    list_url = []

    # Find all the property cards on the page
    for elem in soup.find_all('a', class_="card__title-link"):
        pattern_type = r'/([^/]+)/for-sale'
        match_type = re.search(pattern_type, str(elem))
        type_house = match_type.group(1)
        if type_house != 'new-real-estate-project-apartments':
            list_url.append(elem.get("href"))
            print(elem.get("href"))
    # Print the extracted property links
    return list_url

s = time.perf_counter()

list_houses = []
f = open("items.txt", "r")
for line in f:
    list_houses.append(line)

for url_house in list_houses[0:2]:
    data = []
    house = House(url_house)
    house_info = house.scrape_house()
    print(house_info)
    data.append(house_info)
    print(data)
    df = pd.DataFrame(data)
    df.to_csv('houses.csv', mode='a', index=False, header=False)


elapsed = time.perf_counter() - s
print(f"{__file__} executed in {elapsed:0.2f} seconds.")












