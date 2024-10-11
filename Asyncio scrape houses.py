import asyncio
import time
import pandas as pd
import requests
from requests import Session
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

'''
This file is to scrape the urls of the induvidual houses 
using Asyncio to speed things up
It adds the scraped data in a houses.csv file
'''

# Read the houses in the "items.txt" file and add them in a list
list_houses = []
f = open("items.txt", "r")
for line in f:
    list_houses.append(line)

async def scrape_house(url):
    '''
    An async function to scrape the house url
    '''
    # Set up custom headers
    pattern_type = r'/([^/]+)/for-sale'
    match_type = re.search(pattern_type, url)
    type_house = match_type.group(1)
    # Exclude new-real-estate-project-apartments and new-real-estate-project-houses from the scraping
    if type_house == 'new-real-estate-project-apartments':
        pass
    if type_house == 'new-real-estate-project-houses':
        pass
    else:
        data = []
        try:
            # setup BeautifulSoup
            headers = requests.utils.default_headers()
            headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
                })
            session = Session()
            response = session.get(url, headers=headers)
            print(response.status_code)
            soup = BeautifulSoup(response.content, "html.parser")
            
            # Scrapes table content with tag 'th' from the webpage and adds it to a list
            list_keys = []
            for elem in soup.find_all('th', class_="classified-table__header"):
                print(elem.contents)
                text = " ".join([str(item) for item in elem.contents])
                text = text.replace("\n", "")
                text = " ".join(text.split())

                list_keys.append(text)   
                     
            # Scrapes table content with tag 'td' from the webpage and adds it to a list
            list_info = []
            for elem in soup.find_all('td', class_="classified-table__data"):
                print(elem.contents)
                text = " ".join([str(item) for item in elem.contents])
                text = text.replace("\n", "")
                text = " ".join(text.split())
                print(text)
                list_info.append(text)
                        
            # Create a house_info dictionary and use the 2 lists as key:value pairs
            house_info = {}
            for n in range(len(list_info)):
                house_info[list_keys[n]] = list_info[n]
            print(house_info)
                
            # Use regex to get the property_id from the url
            pattern = r'/(\d+)$'
            match = re.search(pattern, url)
            property_id = match.group(1)

            # Use regex to get the postal code from the url
            pattern_postal_code = r'/(\d{4})/(\d+)$'
            match_postal_code = re.search(pattern_postal_code, url)
            postal_code = match_postal_code.group(1)

            # Use regex to get the locality_name from the url
            pattern_locality_name = r'/([^/]+)/(\d{4})/(\d+)$'
            match_locality_name = re.search(pattern_locality_name, url)
            locality_name = match_locality_name.group(1).capitalize()

            # Use regex to get the type_house from the url
            pattern_type = r'/([^/]+)/for-sale'
            match_type = re.search(pattern_type, url)
            type_house = match_type.group(1)

            # Create an empty house dictionary and add the information we need
            house = {}
            house['Property ID'] = property_id
            house['Locality name'] = locality_name
            house['Postal code'] = postal_code

                #Add price to the house dictionary
            try:
                price = house_info['Price'].split()
                for n in price:
                    if n[0].isdigit():
                        house['price'] = "€" + n
            except:
                house['Price'] = None

            # Add type_house to the house dictionary
            house['Type of property'] = type_house

            # Add Subtype of the house if present on website
            if 'Subtype of property' in house_info:
                house['Subtype of property'] = house_info['Subtype of property']
            else:
                house['Subtype of property'] = None
            
            # Add Number of room to the house dictionary if present on website
            if 'Bedrooms' in house_info:
                house['Number of rooms'] = house_info['Bedrooms']
            else:
                house['Number of rooms'] = None

            # Add surface of the plot to the dictionary
            if 'Surface of the plot' in house_info:
                surface_area = house_info['Surface of the plot'].split()[0]
                surface_area += ' m²'
                house['Surface of the plot'] = surface_area
            else:
                house['Surface of the plot'] = None
            
            # Add living area to house dictionary
            if 'Living area' in house_info:
                area = house_info['Living area'].split()[0]
                area += ' m²'
                house['Living area'] = area
            else:
                house['Living area'] = None

            # Add kitchen to the house dictionary. Info is in binary code
            if 'Kitchen type' or 'Kitchen surface' in house_info:
                house['kitchen'] = 1
            else:
                house['kitchen'] = 0

            # Add furnished to the house dictionary. Info is in binary code
            if 'Furnished' in house_info:
                if house_info['Furnished'] == 'Yes':
                    house['furnished'] = 1
                else:
                    house['furnished'] = 0 
            else:
                house['furnished'] = None

            # Add Open fire to the house dictionary. Info is in binary code
            if 'How many fireplaces?' in house_info:
                if house_info['How many fireplaces?'] != 0:
                    house['Open fire'] = 1
                else:
                    house['Open fire'] = 0
            else:
                house['Open fire'] = None

            # Add Terrace area to the house dictionary
            if 'Terrace surface' in house_info:
                area = house_info['Terrace surface'].split()[0]
                area += ' m²'
                house['Terrace'] = area
            else:
                house['Terrace'] = None
                
            # Add Garden area to the house dictionary
            if 'Garden surface' in house_info:
                garden = house_info['Garden surface'].split()[0]
                garden += ' m²'
                house['Garden'] = garden
            else: 
                house['Garden'] = None 
            
            # Add number of facades to the house dictionary
            if 'Number of frontages' in house_info:
                house['Number of facades'] = house_info['Number of frontages']
            else:
                house['Number of facades'] = None

            # Add swimming pool to the house dictionary
            if 'Swimming pool' in house_info:
                if house_info['Swimming pool'] == 'Yes':
                    house['Swimming pool'] = 1
                else:
                    house['Swimming pool'] = 0
            else:
                house['Swimming pool'] = None

            #A dd state of building to the house dictionary
            if 'Building condition' in house_info:
                house['State of builing'] = house_info['Building condition']
            else:
                house['State of buiding'] = None

            # Add the house to the houses.csv file
            print(house)
            data.append(house)
            df = pd.DataFrame(data)
            df.to_csv('houses.csv', mode='a', index=False, header=False)
        except:
            print("An exception occurred")


async def main():
    # the main async function
    tasks = []

    for n in list_houses[10000:10556]:  # Limit to n number of houses from the items.txt file
        tasks.append(scrape_house(n))
    await asyncio.gather(*tasks)

# Run the main program and display how long it took to run the program
if __name__ == "__main__":
    s = time.perf_counter()
    asyncio.run(main())
    elapsed = time.perf_counter() - s
    print(f"{__file__} executed in {elapsed:0.2f} seconds.")