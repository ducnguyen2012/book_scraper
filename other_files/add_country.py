import requests
import pandas as pd
import random
import os
from dotenv import load_dotenv
load_dotenv()

BOOK_FILE = "./book_scraper/data/books.csv"

def get_countries():

    url = "https://api.restcountries.com/countries/v5"
    headers = {
        "Authorization": f"Bearer {os.getenv('AUTHORIZATION_REST_COUNTRIES')}"
    }
    try: 
        response = requests.get(url, headers=headers)
    except requests.RequestException as e:
        print(f"Error fetching countries: {e}")
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

df=pd.read_csv(
    BOOK_FILE
)

df["publisher_country"] = [
    random.choice(countries)
    for _ in range(len(df))
]

df.to_csv(
    "./book_scraper/data/books_with_country.csv",
    index=False
)
print("Done")