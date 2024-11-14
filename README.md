# 🏢 Immo-eliza-scraping
```
Immo Eliza - Data Collection
Repository: immo-eliza-scraping
Learning Objectives: Use Python to collect as much data as possible.
```
## 📖 Description
```
This project had the following objectives:
    Be able to scrape a website
    Be able to build a dataset from scratch
```    
## 🚀 The Mission
The fictional real estate company "Immo Eliza" wants to develop a machine learning model to make price predictions on real estate sales in Belgium. They hired me to help with the entire pipeline. Immoweb is a commonly used website for Belgian properties.

The first task is to build a dataset that gathers information about at least 10000 properties all over Belgium. This dataset will be used later to train a prediction model.

The final dataset is a csv file with the following 17 columns:
```
Property ID
Locality name
Postal code
Price
Type of property (house or apartment)
Subtype of property (bungalow, chalet, mansion, ...)
Number of rooms
Surface of the plot
Living area (area in m²)
Kitchen (0/1)
Furnished (0/1)
Open fire (0/1)
Terrace (area in m² or null if no terrace)
Garden (area in m² or null if no garden)
Number of facades
Swimming pool (0/1)
State of building (new, to be renovated, ...)
```
## 🔧 Installation
Clone the repository to your local machine
Set up your virtual enviroment and install the packages from the requirements.txt file

## 📦 Repo structure
```
.
├── scraper/
│   └── scraper.py
├── .gitignore
├── main.py
├── Asyncio get urls.py
├── Asyncio scrape houses.py
├── requirements.txt
├── items.txt
├── houses.csv
└── README.md

```

## 🤖 Usage
```
main.py:
the python main.py file contains a function to scrape the url's of houses from the search results page on www.immoweb.be
A house object from the class House() is also created and a function to scrape it is called

Asyncio get urls.py:
This is the file used to create the items.txt containing the url's of the houses from www.immoweb.be

Asyncio scrape house.py:
This the file used to scrape induvidual houses and add the data to houses.csv
```
## ⏱️ Timeline
This project took five days for completion.

## 📚 Sources
www.immoweb.be

This project was done as part of the AI Boocamp at BeCode.org.
