from scraper.scraper import House
from bs4 import BeautifulSoup
import re
import requests
from requests import Session

def scrape_list_of_houses(url):
    '''
    A function to scrape the house urls from the search page on www.immoweb.be
    '''
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

    # Find all the property cards on the page. Exclude new-real-estate-project-apartments
    for elem in soup.find_all('a', class_="card__title-link"):
        pattern_type = r'/([^/]+)/for-sale'
        match_type = re.search(pattern_type, str(elem))
        type_house = match_type.group(1)
        if type_house != 'new-real-estate-project-apartments':
            list_url.append(elem.get("href"))
            print(elem.get("href"))
    # Print the extracted property links
    return list_url


# Create a house object
house = House('https://www.immoweb.be/en/classified/house/for-sale/beveren/8791/20223110')
# Scrape the info from the house object from www.immoweb.be
info = house.scrape_house()
# Print the house info
print(info)











