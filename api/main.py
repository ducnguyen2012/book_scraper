from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd


FILE="../data/books_with_country.csv"

app=FastAPI()
books=pd.read_csv(FILE)

# create schema for API 
class Book(BaseModel):
    title: str
    price: str
    availability: str
    product_link: str
    rating: int
    publisher_country:str


@app.get("/books")
def get_books(
    country:str=None
):

    if country:
        result = books[
            books.publisher_country
            == country
        ]
        return result.to_dict(
            orient="records"
        )
    return books.to_dict(
        orient="records"
    )


@app.post("/books")
def add_book(book:Book):

    global books
    books.loc[len(books)] = book.dict()
    books.to_csv(
        FILE,
        index=False
    )
    return {
        "message":"Book added"
    }


@app.delete("/books/{title}")
def delete_book(title:str):

    global books


    before=len(books)


    books = books[
        books.title != title
    ]


    if len(books)==before:

        raise HTTPException(
            404,
            "Book not found"
        )


    books.to_csv(
        FILE,
        index=False
    )


    return {
        "message":"Deleted"
    }