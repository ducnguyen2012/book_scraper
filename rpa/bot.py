import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
from openpyxl import Workbook

API="http://localhost:8000/books"

# get all books from local API
books=requests.get(API).json()

# filter 5 stars
five_star_books=[
    b for b in books
    if b["rating"]==5
]

logging.info(f"len five_star_books: {len(five_star_books)}")

# Browser setup
options=webdriver.ChromeOptions()

driver=webdriver.Chrome(
    options=options
)

results=[]
for book in five_star_books:
    title = book["title"]

    url = "https://en.wikipedia.org/wiki/Special:Search"

    driver.get(url)

    search_input = WebDriverWait(
        driver,
        10
    ).until(
        EC.presence_of_element_located(
            (
                By.ID,
                "ooui-php-1"
            )
        )
    )

    search_input.send_keys(title)
    search_input.send_keys(Keys.ENTER)

    WebDriverWait(
        driver,
        10
    ).until(
        EC.url_contains("wikipedia.org")
    )

    wikipedia_url = driver.current_url

    results.append({
        "Title": title,
        "Price": book["price"],
        "Publisher Country": book["publisher_country"],
        "Wikipedia URL": wikipedia_url
    })
driver.quit()
# Create Excel
wb=Workbook()

ws=wb.active

ws.title="Report"
ws.append(
    [
        "Title",
        "Price",
        "Publisher Country",
        "Wikipedia URL"
    ]
)



for r in results:
    ws.append(list(r.values()))


wb.save("./rpa/report.xlsx")
logging.info("Report generated")