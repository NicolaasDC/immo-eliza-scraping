from scraper.scraper import House
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re

def scrape_list_of_houses(url):
    #--| Setup
    options = Options()
    browser = webdriver.Chrome(options=options)
    #--| Parse or automation
    browser.get(url)
    time.sleep(1)

    # Use BeautifulSoup
    soup = BeautifulSoup(browser.page_source, "html.parser")
    list_url = []
    for elem in soup.find_all('a', class_="card__title-link"):
        list_url.append(elem.get("href"))

    return list_url


list_houses = scrape_list_of_houses('https://www.immoweb.be/nl/zoeken/huis/te-koop?countries=BE&page=1&orderBy=relevance')
print(list_houses)

for url_house in list_houses:
    house = House(url_house)
    house_info = house.scrape_house()
    print(house_info)



