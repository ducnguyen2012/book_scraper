import pytest
from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_get_all_books():
    """
    Test GET /books
    """
    response = client.get("/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_get_books_by_country():
    """
    Test GET /books?country=
    """
    response = client.get(
        "/books?country=Japan"
    )
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    for book in data:
        assert book["publisher_country"] == "Japan"

def test_add_new_book():
    """
    Test POST /books
    """
    new_book = {
        "title": "Testing FastAPI Book",
        "price": "£20",
        "availability": "In stock",
        "product_link": 
        "https://example.com",
        "rating": 5,
        "publisher_country": "Vietnam"
    }
    response = client.post(
        "/books",
        json=new_book
    )
    assert response.status_code in [
        200,
        201
    ]
    data = response.json()
    assert data["message"] == "Book added"

def test_delete_book():
    """
    Test DELETE /books/{title}
    """
    response = client.delete(
        "/books/Testing%20FastAPI%20Book"
    )
    assert response.status_code == 200

def test_invalid_endpoint():
    response = client.get(
        "/wrong"
    )
    assert response.status_code == 404