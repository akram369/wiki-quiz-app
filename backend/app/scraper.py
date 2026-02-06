import requests
import re
from bs4 import BeautifulSoup

EDITORIAL_PHRASES = [
    "this article",
    "this page",
    "for other uses",
    "may refer to",
    "this is an accepted"
]


def clean_text(text: str) -> str:
    return re.sub(r"\[\d+\]", "", text).strip()


def scrape_wikipedia(url: str) -> dict:
    response = requests.get(
        url,
        headers={"User-Agent": "WikiQuizBot/1.0"},
        timeout=15
    )
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find("h1", id="firstHeading")
    title = title_tag.get_text(strip=True) if title_tag else "Unknown"

    content_div = soup.find("div", class_="mw-parser-output")
    if not content_div:
        raise ValueError("Wikipedia content not found")

    summary = ""
    for p in content_div.find_all("p"):
        text = clean_text(p.get_text(" ", strip=True))
        if not text:
            continue
        if any(phrase in text.lower() for phrase in EDITORIAL_PHRASES):
            continue
        if len(text.split()) >= 10:
            summary = text
            break

    if not summary:
        summary = f"{title} is a notable subject documented on Wikipedia."

    sections = []
    for h2 in content_div.find_all("h2"):
        span = h2.find("span", class_="mw-headline")
        if span:
            sections.append(span.get_text(strip=True))

    return {
        "title": title,
        "summary": summary,
        "sections": sections,
        "raw_html": response.text
    }
