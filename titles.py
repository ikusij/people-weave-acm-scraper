from bs4 import BeautifulSoup
import requests
import json

def get_page(url: str) -> BeautifulSoup:
    page = requests.get(url)
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def get_page_data(soup: BeautifulSoup) -> list[str]:

    conference_abb = list()
    conferences = dict()

    cards = soup.select("li.search__item")
    for card in cards:
        conference_abb.append(card["class"][-1])
        title = card.select_one("span.browse-title").text.strip()
        description = card.select_one("div.meta__abstract").text.strip()
        conferences[title] = {
            "description": description
        }
    
    with open("titles.json", "w") as file:
        json_object = json.dumps(conferences, indent = 4)
        file.write(json_object)
    
    return conference_abb

def main() -> list[str]:
    soup = get_page("https://dl.acm.org/conferences")
    conference_abb = get_page_data(soup)
    return conference_abb