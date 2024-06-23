import requests
from bs4 import BeautifulSoup
import pandas as pd
import hashlib
import urllib.parse
import os

def get_article_links(url, page_index):
    response = requests.get(url + f"&start={page_index}")
    if response.status_code != 200:
        print(f"Failed to fetch page {page_index}, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.select("div.info_group")
    links = [article.select("a.info")[1].attrs["href"] for article in articles if len(article.select("a.info")) >= 2]
    return links

def get_article_content(url):
    response = requests.get(url, headers={'User-agent': 'Mozilla/5.0'})
    if response.status_code != 200:
        print(f"Failed to fetch article from {url}, status code: {response.status_code}")
        return None, None, None

    soup = BeautifulSoup(response.text, "html.parser")
    title = soup.select_one(".media_end_head_headline")
    content = soup.select_one("#dic_area")
    date = soup.select_one(".media_end_head_info_datestamp_time")

    if not title or not content or not date:
        print(f"Failed to parse article from {url}")
        return None, None, None

    return title.text.strip(), content.text.strip(), date.text.strip()

def fetch_news_articles(base_url, search_query, start_date, end_date, output_dir):
    articles_data = []
    seen_urls = set()
    seen_hashes = set()
    page_num = 1
    page_index = 1

    encoded_query = urllib.parse.quote(search_query)
    search_url = base_url.format(query=encoded_query, start_date=start_date, end_date=end_date)

    while True:
        print(f"Fetching page {page_num} for query '{search_query}'...")
        article_links = get_article_links(search_url, page_index)

        if not article_links:
            print(f"No more articles found at page {page_num}. Ending fetch.")
            break

        for url in article_links:
            if url in seen_urls:
                continue

            title, content, date = get_article_content(url)
            if not title or not content or not date:
                continue

            content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
            if content_hash in seen_hashes:
                continue

            articles_data.append([url, title, content, date])
            seen_urls.add(url)
            seen_hashes.add(content_hash)

        if page_num % 10 == 0:
            df = pd.DataFrame(articles_data, columns=["URL", "Title", "Content", "Date"])
            df.to_excel(os.path.join(output_dir, f"news_articles_result_{search_query}_{start_date}_to_{end_date}.xlsx"), index=False, engine='openpyxl')
            print(f"Saved up to page {page_num} for query '{search_query}'")

        page_num += 1
        page_index += 10

    df = pd.DataFrame(articles_data, columns=["URL", "Title", "Content", "Date"])
    df.to_excel(os.path.join(output_dir, f"news_articles_result_{search_query}_{start_date}_to_{end_date}.xlsx"), index=False, engine='openpyxl')
    print(f"Final data saved for query '{search_query}'")

# Define the base URL
base_url = "https://search.naver.com/search.naver?where=news&query={query}&sm=tab_opt&sort=0&photo=2&field=0&pd=3&ds={start_date}&de={end_date}&docid=&related=0&mynews=0&office_type=0&office_section_code=0&news_office_checked=&nso=so%3Ar%2Cp%3Afrom{start_date}to{end_date}&is_sug_officeid=0&office_category=0&service_area=0"

# Define the date ranges
date_ranges = [
 #   ("2022.11.15", "2023.09.29"),
    ("2023.09.30", "2024.04.30"),
]

# Specify the output directory
output_dir = r'C:\Users\user\Downloads'

keywords = [
    'tv'
]

# 각 키워드와 날짜 범위에 대해 기사 수집
for keyword in keywords:
    for start_date, end_date in date_ranges:
        fetch_news_articles(base_url, keyword, start_date, end_date, output_dir)
