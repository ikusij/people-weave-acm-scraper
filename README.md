# people-weave-acm-scraper

## Overview

The purpose of this script is to scrape and parse data from all the conferences listed in https://dl.acm.org/conferences. 

Each conference is formatted as follows:

```javascript

"ACM Southeast Regional Conference": {
    "description": "ACM Southeast Regional Conference the oldest, continuously running, annual conference of the ACM. ACMSE provides an excellent forum for both faculty and students to present their research in a friendly and dynamic atmosphere in all areas of computer science.",
    "pub_years": [
        1967,
        2023
    ],
    "pub_count": 2409,
    "available_for_download": 2287,
    "citation_count": 6583,
    "cum_downloads": 710835,
    "average_citations_per_article": 3,
    "average_downloads_per_article": 311,
    "upcomming_conferences": {},
    "proceedings": {
        "0": {
            "name": "ACMSE 2023: Proceedings of the 2023 ACM Southeast Conference",
            "description": "ACM SE: ACM Southeast Regional Conference"
        },
        "1": {
            "name": "ACM SE '22: Proceedings of the 2022 ACM Southeast Conference",
            "description": "ACM SE: ACM Southeast Regional Conference"
        },
        "2": {
            "name": "ACM SE '21: Proceedings of the 2021 ACM Southeast Conference",
            "description": "ACM SE: ACM Southeast Regional Conference"
        },
        "3": {
            "name": "ACM SE '20: Proceedings of the 2020 ACM Southeast Conference",
            "description": "ACM SE: ACM Southeast Regional Conference"
        }
    },
    "subject_areas": [
        "Computer science education",
        "Human computer interaction (HCI)",
        "Information science education",
        "Neural networks",
        "Machine learning",
        "Education",
        "Language types",
        "Information retrieval",
        "Mobile networks",
        "Language features",
        "Data mining",
        "Software testing and debugging",
        "Computer crime",
        "Software development process management",
        "Computer-assisted instruction",
        "Network protocols",
        "Performance",
        "Security and privacy",
        "Compilers",
        "Database design and models"
    ],
    "most_freq_affiliations": {
        "0": {
            "university": "Auburn University",
            "paper_count": 127
        },
        "1": {
            "university": "Clemson University",
            "paper_count": 124
        },
        "2": {
            "university": "Kennesaw State University",
            "paper_count": 109
        },
        "3": {
            "university": "The University of Alabama",
            "paper_count": 106
        },
        "4": {
            "university": "The University of Alabama in Huntsville",
            "paper_count": 80
        }
    },
    "most_cited_authors": {
        "0": {
            "name": "Edmund Melson Clarke, Jr.",
            "university_affiliation": "Carnegie Mellon University"
        },
        "1": {
            "name": "GailJoon  Ahn",
            "university_affiliation": "Arizona State University"
        },
        "2": {
            "name": "Mark J. Guzdial",
            "university_affiliation": "University of Michigan, Ann Arbor"
        },
        "3": {
            "name": "Thomas Jaudon Ball",
            "university_affiliation": "Microsoft Corporation"
        },
        "4": {
            "name": "S Sahni",
            "university_affiliation": "University of Florida"
        }
    },
    "recent_award_winners": {
        "0": {
            "name": "Satoshi  Matsuoka",
            "award": "2021 ACM Gordon Bell Prize"
        },
        "1": {
            "name": "Trevor Nigel Mudge",
            "award": "2014 ACM-IEEE CS Eckert-Mauchly Award"
        },
        "2": {
            "name": "Akira  Nukada",
            "award": "2011 ACM Gordon Bell Prize"
        },
        "3": {
            "name": "Takayuki  Aoki",
            "award": "2011 ACM Gordon Bell Prize"
        },
        "4": {
            "name": "J. Irwin",
            "award": "2010 ACM Athena Lecturer Award"
        },
        "5": {
            "name": "Kiyoshi  Oguri",
            "award": "2009 ACM Gordon Bell Prize"
        },
        "6": {
            "name": "Edmund Melson Clarke, Jr.",
            "award": "2007 ACM A. M. Turing Award"
        },
        "7": {
            "name": "Aseem  Agarwala",
            "award": "2006 ACM Doctoral Dissertation Award"
        },
        "8": {
            "name": "Robert King Brayton",
            "award": "2006 ACM Paris Kanellakis Theory and Practice Award"
        },
        "9": {
            "name": "Wen Mei W Hwu",
            "award": "1999 ACM Grace Murray Hopper Award"
        }
    }
}

```

## Running the Script

Run the following commands to clone the project and download any nessecary python libraries

```bash
git clone https://github.com/ikusij/people-weave-acm-scraper.git
```

Once we've successfully copied the repository, run the following commands

### In Windows

```bash
python -m venv venv
source venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

### In Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip3 install -r requirements.txt
```

Once we've setup the repository correctly, run the following command

### In Windows

```bash
python main.py
```

### In Mac

```bash
python3 main.py
```

Now the script takes a while to run since we've naively added a 1min sleep between scraping each conference to avoid being blocked by the website. 

## Features

The website loads data dynamically for the following sections:

- Most Frequent Affiliations
- Most Cited Authors
- Recent Award Winners

Rather than using a library such as Selenium to scrape the dynamically loaded data, which has substantial overhead, we'll use hidden api requests by the website to get the dynamic data. In doing so, we reduce overhead and improve running time. 

## Further Scope

We can further improve the performance of our scraper by doing the following:

1) Add asynchronous request handling when scraping the dynamically loaded data since we need to request 3 different urls.
2) Add proxies to avoid getting blocked by the website. This would replace the naive sleep call. 
