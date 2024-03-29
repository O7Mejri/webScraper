# Web Scrapers for LinkedIn and Crunchbase

## Overview
This project includes web scrapers for extracting data from LinkedIn job listings and Crunchbase company profiles. The scrapers gather relevant information such as job titles, company names, locations, industries, and more.

## LinkedIn Scraper
The LinkedIn scraper extracts job listings for Data Analyst positions. It collects details such as job title, company name, location, and date listed.

## Crunchbase Scraper
The Crunchbase scraper extracts information on companies in the SAAS industry. It retrieves data including company name, industry, and location.

## Installation
1. Clone the repository: `git clone https://github.com/O7Mejri/webScraper.git`
2. Install dependencies: `pip install -r requirements.txt`

## Usage
1. Configure the PostgreSQL database settings in the `settings.py` file.
2. Run the LinkedIn scraper: `scrapy crawl linkedin_jobs`
3. Run the Crunchbase scraper: `scrapy crawl crunchbase_scraper`

## Database
Scraped data is stored in a PostgreSQL database. Ensure PostgreSQL is installed and configure the database settings in the `settings.py` file.

## Dependencies
- Python 3.x
- Scrapy
- Psycopg2 (for PostgreSQL)

