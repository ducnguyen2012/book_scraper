# Book Scraper Automation System

An end-to-end automation project that combines:

- Web Scraping & Crawling
- External API Integration
- REST API Development
- RPA Browser Automation
- Automated Report Generation


## System Overview

The system performs the following pipeline:

1. Scrape books from `https://books.toscrape.com`
2. Save book information and HTML backup
3. Enrich book data with random publisher country using REST Countries API
4. Provide book data through FastAPI REST API
5. Use Selenium RPA bot to:
   - Consume the API
   - Filter 5-star books
   - Search books on Wikipedia
   - Generate Excel report


## Architecture


```mermaid
flowchart LR

A[Books To Scrape Website]
--> B[Python Scraper]

B --> C[books.csv]

C --> D[REST Countries API]

D --> E[books_with_country.csv]

E --> F[FastAPI Backend]

F --> G[Selenium RPA Bot]

G --> H[Wikipedia]

G --> I[Excel Report]


# Setup and Installation Guide

## 1. Install Conda Environment

This project uses **Conda** to manage the Python environment.

If you do not have Conda installed, please download and install the official Conda distribution:

- Anaconda: https://www.anaconda.com/download
- Miniconda: https://docs.conda.io/projects/miniconda/en/latest/


After installation, verify that Conda is available:

```bash
conda --version
conda create -n bookscraper python=3.11 -y
cd book_scraper 
pip install -r requirements.txt


## Docker Deployment


Build image:

```bash
sudo docker build -t book-scraper-api .


run: 
sudo docker run -p 8000:8000 book-scraper-api



---

swagger
http://localhost:8000/docs

Với assignment này, mình khuyên bạn nộp:

- Dockerfile cho FastAPI
- docker-compose có Redis
- README hướng dẫn build/run

Không nhất thiết phải dockerize Selenium vì RPA thường chạy như một worker riêng. Cách tách API container + RPA worker là kiến trúc thực tế hơn.


set up resdis: 
# Redis Installation and Setup

This project uses Redis as a caching layer to reduce repeated calls to the REST Countries API.

Redis stores API responses temporarily, allowing the application to reuse cached data instead of sending duplicate requests.

---

## 1. Install Redis

### Ubuntu / Linux

Update package list:

```bash
sudo apt update

sudo apt install redis-server

redis-server --version

hãy đảm bảo bạn đã cd vào folder book_scraper.