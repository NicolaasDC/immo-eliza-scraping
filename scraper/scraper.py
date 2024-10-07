from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
 
#--| Setup
options = Options()
browser = webdriver.Chrome(options=options)
#--| Parse or automation
url = "https://www.immoweb.be/nl/zoekertje/uitzonderlijk-vastgoed/te-koop/oosterzele/9860/20197299"
browser.get(url)
time.sleep(1)

# Use BeautifulSoup

soup = BeautifulSoup(browser.page_source, "html.parser")
list_keys = []
for elem in soup.find_all('th', class_="classified-table__header"):
    text = elem.text.replace("\n", "")
    text = " ".join(text.split())
    list_keys.append(text)

list_info = []
for elem in soup.find_all('td', class_="classified-table__data"):
    text = elem.text.replace("\n", "")
    text = " ".join(text.split())
    list_info.append(text)

house = {}
for n in range(len(list)):
    house[list_keys[n]] = list_info[n]

print(house)


