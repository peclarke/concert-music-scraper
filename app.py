import requests
from bs4 import BeautifulSoup

NUM_PER_PAGE = 64

ROOT = "https://www.jwpepper.com"
URL = "https://www.jwpepper.com/sheet-music/search.jsp?redirect=concert-contest-band-music&perPage=" + str(NUM_PER_PAGE)
page = requests.get(URL)
soup = BeautifulSoup(page.content, "html.parser")

def query_website():

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
        link = block.find("a", class_="scoreView")

        video_element = block.find("div", class_="prodMedia-watch")
        video_link = video_element.find_next("a", class_="media-link")

        if link is not None:
            link_text = ROOT + link['href']

            info = {
                'title': title_element,
                'composer': composer_element,
                'publisher': publisher_element,
                'level': level,
                'link': link_text
            }

            if video_link:
                # sometimes does audio too
                info['video'] = video_link["onclick"][25:110].replace("',", "").replace("'", "")

            sources.append(info)

    return sources

def json_to_spreadsheet():
    pass



res = query_website()
print(res)

# print(len('http://www.jwpepper.com/sheet-music/media-player.jsp?&type=audio&productID=10520991E'))