import requests
import pandas as pd
import random
import os
from dotenv import load_dotenv
import logging
load_dotenv()

BOOK_FILE = "./data/books.csv"

def get_countries():

    url = "https://api.restcountries.com/countries/v5"
    headers = {
        "Authorization": f"Bearer {os.getenv('AUTHORIZATION_REST_COUNTRIES')}"
    }
    try: 
        response = requests.get(url, headers=headers)
    except requests.RequestException as e:
        logging.info(f"Error fetching countries: {e}")
        return []

    data = response.json()
    data = data.get("data", {}).get("objects", [])
    countries=[]

    for c in data:

        countries.append(
            c["names"]["common"]
        )

    return countries

countries=get_countries()
if not countries:
    raise ValueError(
        "Country list is empty!"
    )
df=pd.read_csv(
    BOOK_FILE
)

df["publisher_country"] = [
    random.choice(countries)
    for _ in range(len(df))
]

df.to_csv(
    "./data/books_with_country.csv",
    index=False
)
logging.info("Done")