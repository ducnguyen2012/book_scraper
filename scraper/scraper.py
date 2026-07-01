import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
from urllib.parse import urljoin
import time
import logging

BASE_URL = "https://books.toscrape.com"
CATEGORY_URL = (
    "https://books.toscrape.com/"
    "catalogue/category/books/historical-fiction_4/index.html"
)

# build backup folder if not exists
BACKUP_DIR = "./html_backup"
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)
LOG_DIR = "./log/"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("./log/scraper.log")])

def convert_rating(text):
    """
    ratings in website are in text format in class star-rating attribute.
    """
    ratings = {
        "One":1,
        "Two":2,
        "Three":3,
        "Four":4,
        "Five":5
    }
    return ratings[text]

def scrape_category_page(url):
    """
    scrap category page based on url
    """
    html = requests.get(url).text

    soup = BeautifulSoup(
        html,
        "html.parser"
    )
    return soup.find_all(
        "article",
        class_="product_pod"
    )

def get_product_links(books,url):
    """
    preprocess data to get href.
    """
    result=[]
    for book in books:
        link = book.h3.a["href"]
        result.append(
            urljoin(url,link)
        )
    return result

def scrape_product_page(url,index):
    try:
        response=requests.get(url)
    except requests.RequestException as e:
        logging.error(f"Error fetching in scrape_product_page {url}: {e}")
        return None
    time.sleep(1)
    # backup html
    with open(
        f"{BACKUP_DIR}/book_{index}.html",
        "w",
        encoding="utf-8"
    ) as f:
        f.write(response.text)

    soup=BeautifulSoup(
        response.text,
        "html.parser"
    )

    # retrieve all requirement data from product page
    title=soup.h1.text.strip()
    price=soup.find(
        "p",
        class_="price_color"
    ).text
    availability=soup.find(
        "p",
        class_="instock availability"
    ).text.strip()
    rating=soup.find(
        "p",
        class_="star-rating"
    )["class"][1]

    return {
        "title":title,
        "price":price,
        "availability":availability,
        "product_link":url,
        "rating":convert_rating(rating)
    }

# =========== running main function ==============
books_data=[]
for page in range(1,4): # make sure at least 3 pages is scrapped
    logging.info(f"Page {page}")
    if page==1:
        # first page dont have page_num in url
        url=CATEGORY_URL
    else:
        url=(
            "https://books.toscrape.com/"
            "catalogue/category/books/"
            f"science_22/page-{page}.html"
        )

    books=scrape_category_page(url)
    links=get_product_links(
        books,
        url
    )
    for link in links:
        data=scrape_product_page(
            link,
            len(books_data)+1
        )
        books_data.append(data)

df=pd.DataFrame(
    books_data
)
df.to_csv(
    "./data/books.csv",
    index=False
)

logging.info(f"Done! {len(df)} books scraped")
