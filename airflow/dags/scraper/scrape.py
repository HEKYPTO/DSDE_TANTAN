#scrape.py

import os
import requests
from bs4 import BeautifulSoup
import json
from urllib.parse import quote

def scrape_nature(date_range=None, subject=None):
    encoded_date_range = quote(date_range) if date_range else None
    encoded_subject = quote(subject)
    url = f"https://www.nature.com/search?article_type=research&subject={encoded_subject}&order=relevance"
    if encoded_date_range:
        url += f"&date_range={encoded_date_range}"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    articles = soup.find_all("article", class_="u-full-height c-card c-card--flush")
    article_data = []

    for i, article in enumerate(articles):
        if i == 10:
            break
        title = article.find("h3", class_="c-card__title").text.strip()
        link = "https://www.nature.com" + article.find("a", class_="c-card__link u-link-inherit").get("href")
        summary_tag = article.find("div", class_="c-card__summary")
        summary = summary_tag.text.strip() if summary_tag else ""
        author_list = article.find("ul", class_="c-author-list c-author-list--compact c-author-list--truncated")
        authors = [author.text.strip() for author in author_list.find_all("span", itemprop="name")] if author_list else [""]
        article_type = article.find("span", class_="c-meta__type").text.strip()
        open_access = article.find("span", class_="u-color-open-access").text.strip() if article.find("span", class_="u-color-open-access") else ""
        publication_date = article.find("time", itemprop="datePublished").text.strip()
        journal_title = article.find("div", class_="c-meta__item c-meta__item--block-at-lg u-text-bold").text.strip()
        volume_and_pages_tag = article.find("div", class_="c-meta__item c-meta__item--block-at-lg")
        volume_and_pages = volume_and_pages_tag.text.strip() if volume_and_pages_tag else ""

        article_info = {
            "Title": title,
            "Link": link,
            "Summary": summary,
            "Authors": authors,
            "Article Type": article_type,
            "Open Access": open_access,
            "Publication Date": publication_date,
            "Journal Title": journal_title,
            "Volume and Pages": volume_and_pages
        }
        article_data.append(article_info)

    return article_data

def save_json(data, folder_path, file_name):
    json_data = json.dumps(data, indent=4)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    file_path = os.path.join(folder_path, file_name)
    with open(file_path, 'w') as json_file:
        json_file.write(json_data)
    print("JSON data saved to:", file_path)
        
def scrape():
    date_range_lists = ["2018-2018", "2019-2019", "2020-2020", "2021-2021", "2022-2022", "2023-2023"]
    subjects = ["biochemistry", "biophysics", "biotechnology", "cancer", "cell-biology", "chemical-biology",
                "chemistry", "computational-biology-and-bioinformatics", "diseases", "drug-discovery", "genetics",
                "health-care", "immunology", "medical-research", "microbiology", "molecular-biology", "neuroscience",
                "pathogenesis", "physiology", "risk-factors"]
    
    for subject in subjects:
        for date_range in date_range_lists:
            article_data = scrape_nature(date_range, subject)
            folder_path = 'data/nature_json'
            file_name = f"research_{subject}_{date_range.replace('-', '_')}.json"
            save_json(article_data, folder_path, file_name)

