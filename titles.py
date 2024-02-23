from bs4 import BeautifulSoup
import requests
import json

def get_page(url: str) -> BeautifulSoup:

    """
    Helper function that GETS the data from the requested
    url and returns a BeautifulSoup object of the parsed html
    """

    page = requests.get(url)
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def get_page_data(soup: BeautifulSoup) -> list[str]:

    """
    Helper function that scrapes the necessary information
    for the titles.json file and creates it.

    Furthermore, it returns a list of the abbreviated conference 
    names. These abbreviations will be used to scrape the information
    from each conference.
    """

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
    
    """
    Wrapper function to get the necessary information 
    for the titles.json file and create it.
    """

    soup = get_page("https://dl.acm.org/conferences")
    conference_abb = get_page_data(soup)
    return conference_abb