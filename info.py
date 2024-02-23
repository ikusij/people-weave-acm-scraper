from bs4 import BeautifulSoup
import requests
import json
import re

def get_page(url: str) -> BeautifulSoup:

    """
    Helper function that GETS the data from the requested
    url and returns a BeautifulSoup object of the parsed html
    """

    page = requests.get(url)
    page.encoding = "utf-8"
    soup = BeautifulSoup(page.text, "html.parser")
    return soup

def get_bibliometrics(soup: BeautifulSoup, json_object: dict) -> None:

    """
    Helper function that scrapes the bibliometric
    information of a given conference. The data will 
    be appended to the titles.json to create the 
    info.json file as specified. 
    """

    keys = ["pub_count", "available_for_download", "citation_count", "cum_downloads", "average_citations_per_article", "average_downloads_per_article"]
    bibliometrics = soup.select("div.bibliometrics__count")

    pub_years = bibliometrics[0].text.strip().split(" - ")
    json_object["pub_years"] = [ int(pub_years[0]), int(pub_years[1]) ]
    
    bibliometrics = bibliometrics[1:5] + bibliometrics[7:]
    for key, bibliometric in zip(keys, bibliometrics):
        json_object[key] = int(bibliometric.text.strip().replace(",", ""))

def get_upcoming(soup: BeautifulSoup, json_object: dict) -> None:

    """
    Helper function that scrapes the upcoming conferences
    information of a given conference. The data will 
    be appended to the titles.json to create the 
    info.json file as specified. 
    """

    name = soup.select_one("a.event__title")
    info = soup.select("div.info span")

    json_object["upcomming_conferences"] = dict()

    if (not name or not info):
        return

    json_object["upcomming_conferences"][0] = {
        "name": name.text.strip(),
        "date": info[0].text.strip(),
        "location": re.sub("\s", "", info[1].text).replace(",", ", ")
    }

def get_proceedings(soup: BeautifulSoup, json_object: dict) -> None:

    """
    Helper function that scrapes the proceedings
    information of a given conference. The data will 
    be appended to the titles.json to create the 
    info.json file as specified. 
    """

    json_object["proceedings"] = dict()

    blocks = soup.select("li.active ul.rlist li.grid-item")
    for index, block in enumerate(blocks):
       
        name = block.select_one("h3")
        if (name):
            name = name.text.strip()
        description = block.select_one("li")
        if (description):
            description = description.text.strip()
        
        json_object["proceedings"][index] = {
            "name": name,
            "description": description
        }

def get_subject_areas(soup: BeautifulSoup, json_object: dict) -> None:

    """
    Helper function that scrapes the subject areas
    information of a given conference. The data will 
    be appended to the titles.json to create the 
    info.json file as specified. 
    """

    block = soup.find("div", attrs = { "data-tags": True })["data-tags"]
    subject_areas = re.findall("\"label\":\"(.*?)\"", block)
    json_object["subject_areas"] = subject_areas

def get_dynamically_loaded(soup: BeautifulSoup, json_object: dict) -> None:

    """
    Helper function that requests the information for
    the affiliations, authors, and awards sections 
    to be scraped for the info.json file. 
    """

    affiliations, authors = soup.find_all(attrs = { "data-ajaxurl": True })

    get_affiliations(affiliations["data-ajaxurl"], json_object)
    get_authors(authors["data-ajaxurl"], json_object)

    awards = soup.find(attrs = { "data-ajaxlink": True })
    get_awards(awards["data-ajaxlink"], json_object)
    
def get_affiliations(ajax: str, json_object: dict):
    
    """
    Helper function that scrapes the affiliation
    information of a given conference. The data will 
    be appended to the titles.json to create the 
    info.json file as specified. 
    """

    text = requests.get(f"https://dl.acm.org{ajax}").text

    data = re.findall("\"data\":\[(.*?)\]", text)[0]
    entries = re.findall("\{(.*?)\}", data)
    
    json_object["most_freq_affiliations"] = dict()

    for index, entry in enumerate(entries):
        
        json_entry = json.loads("{" + entry + "}")
        paper_count = int(json_entry["count"])
        soup_entry = BeautifulSoup(json_entry["content"], "html.parser")
        university = soup_entry.select_one("h5 > a").text.strip()

        json_object["most_freq_affiliations"][index] = {
            "university": university, 
            "paper_count": paper_count
        }

def get_authors(ajax: str, json_object: dict):

    """
    Helper function that scrapes the author
    information of a given conference. The data will 
    be appended to the titles.json to create the 
    info.json file as specified. 
    """

    text = requests.get(f"https://dl.acm.org{ajax}").text

    data = re.findall("\"data\":\[(.*?)\]", text)[0]
    entries = re.findall("\{(.*?)\}", data)

    json_object["most_cited_authors"] = dict()

    for index, entry in enumerate(entries):
        
        json_entry = json.loads("{" + entry + "}")
        soup_entry = BeautifulSoup(json_entry["content"], "html.parser")
        name = soup_entry.select_one("div.box-item__title-holder a").text.strip()
        university_affiliation = soup_entry.select_one("div.box-item__title-holder span").text.strip()

        json_object["most_cited_authors"][index] = {
            "name": name, 
            "university_affiliation": university_affiliation
        }

def get_awards(ajax: str, json_object: dict):

    """
    Helper function that scrapes the award
    information of a given conference. The data will 
    be appended to the titles.json to create the 
    info.json file as specified. 
    """

    response = requests.get(f"https://dl.acm.org{ajax}&pbContext=%3Btaxonomy%3Ataxonomy%3Aconference-collections%3Bpage%3Astring%3AHome%3Bwgroup%3Astring%3AACM%20Publication%20Websites%3Bcsubtype%3Astring%3AConference%3Bctype%3Astring%3AConference%20Content%3Bwebsite%3Awebsite%3Adl-site%3Btopic%3Atopic%3Aconference-collections%3Easpdac%3BpageGroup%3Astring%3APublication%20Pages").text
    data = json.loads(response)
    
    json_object["recent_award_winners"] = dict()

    for index, entry in enumerate(data["data"]["results"]):
        
        award = entry["title"]
        content = entry["content"]
        soup_content = BeautifulSoup(content, "html.parser")
        name = soup_content.select_one("div.creative-work__content a").text.strip()
        
        json_object["recent_award_winners"][index] = {
            "name": name,
            "award": award
        }

def main(abb: str, json_object: dict):

    """
    Wrapper function to get the necessary information 
    for the info.json file and create it by appending
    data to a copy of the titles.json file. 
    """

    soup = get_page(f"https://dl.acm.org/conference/{abb}")

    get_bibliometrics(soup, json_object)
    get_upcoming(soup, json_object)
    get_proceedings(soup, json_object)
    get_subject_areas(soup, json_object)
    get_dynamically_loaded(soup, json_object)
