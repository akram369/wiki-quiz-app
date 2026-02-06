import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url: str):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").text
    paragraphs = soup.select("p")
    summary = " ".join(p.text for p in paragraphs[:2])

    sections = [
        h.text for h in soup.select("h2 span.mw-headline")
    ]

    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "raw_html": response.text
    }
