import math
import requests
import pandas
import os
import json

from bs4 import BeautifulSoup

# don't change these
MAX_PER_PAGE = 100
ROOT = "https://www.jwpepper.com"

# Changeable Values
NUMBER = 400 # Number of Scores to Generate

def generate_urls():
    factor = math.ceil(NUMBER / MAX_PER_PAGE)
    # print(factor)
    urls = []
    for i in range(factor):
        start = MAX_PER_PAGE * i

        if NUMBER - MAX_PER_PAGE * i < 100:
            pageNum = NUMBER - MAX_PER_PAGE
        else:
            pageNum = MAX_PER_PAGE

        url = f"https://www.jwpepper.com/sheet-music/search.jsp?pageview=list-view&perPage={pageNum}&perPage={pageNum}&redirect=concert-contest-band-music&startIndex={start}&perPage={pageNum}"
        urls.append(url)
    return urls

def query_website(soup):

    sources = []

    blocks = soup.find_all("div", class_="results-product-block")

    for block in blocks:
        title_element = block.find("a", class_="titlelink").text.strip()
        composer_element = block.find("span", class_="composer-name").text.strip()
        publisher_element = block.find("span", class_="publisher-name").text.replace("-","").strip()

        level_element = block.find("div", class_="results-linked-grid-items")
        level_area = level_element.find_next("div", class_="prodLevel")
        level = level_area.find("span").text.replace("\n", "")

        media_element = block.find("span", class_="prodMedia-icons")
        audio_link = block.find("a", class_="scoreView")

        video_element = block.find("div", class_="prodMedia-watch")
        video_link = video_element.find_next("a", class_="media-link")

        info = {
            'title': title_element,
            'composer': composer_element,
            'publisher': publisher_element,
            'level': level
        }

        # get the links for the score

        if audio_link:
            link_text = ROOT + audio_link['href']
            info['audio-link'] = link_text

        if video_link:
            link = video_link["onclick"][25:110].replace("',", "").replace("'", "")
            if "audio" not in link:
                info['video-link'] = link

        sources.append(info)

    return sources

def query_all():
    urls = generate_urls()
    print("Starting website scraping...")
    all_scores = []
    for url in urls:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        scores = query_website(soup)
        all_scores = all_scores + scores
    return all_scores

def json_to_spreadsheet(res):
    # delete previous
    if os.path.exists("./outputs/results.json"):       
        os.remove('./outputs/results.json')
    # make the json file
    f = open("./outputs/results.json", "a")
    json_obj = json.dumps(res)
    f.write(json_obj)
    f.close()

    pandas.read_json("./outputs/results.json").to_excel("./outputs/output.xlsx")


def main():
    res = query_all()
    print("Finished scraping website and formatting results")
    json_to_spreadsheet(res)
    print("Finished generating spreadsheet")

main()