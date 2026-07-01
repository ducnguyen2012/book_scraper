import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from openpyxl import Workbook

API="http://localhost:8000/books"

# =====================
# Get books from API
# =====================

books=requests.get(API).json()

five_star_books=[
    b for b in books
    if b["rating"]==5
]

print(f"len five_star_books: {len(five_star_books)}")



# =====================
# Browser setup
# =====================


options=webdriver.ChromeOptions()

driver=webdriver.Chrome(
    options=options
)

results=[]

for book in five_star_books:
    title=book["title"]


    driver.get(
        "https://en.wikipedia.org/"
    )
    search_button = WebDriverWait(
        driver,
        5
    ).until(
        EC.element_to_be_clickable(
            (
                By.CSS_SELECTOR,
                ".vector-icon.mw-ui-icon-search.mw-ui-icon-wikimedia-search.cdx-button__icon"
            )
        )
    )

    search_button.click()

    search_input = WebDriverWait(
        driver,
        10
    ).until(
        EC.element_to_be_clickable(
            (
                By.ID,
                "searchInput"
            )
        )
    )


    search_input.send_keys(title)
    search_input.send_keys(Keys.ENTER)


    time.sleep(2)



    try:

        url=driver.current_url


    except:

        url="No result"



    results.append({

        "Title":title,

        "Price":book["price"],

        "Publisher Country":
        book["publisher_country"],

        "Wikipedia URL":
        url

    })



driver.quit()



# =====================
# Create Excel
# =====================


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

    ws.append(
        list(r.values())
    )


wb.save(
    "report.xlsx"
)


print(
"Report generated"
)