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
