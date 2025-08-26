import re
import sys
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

EA_NEWS_INDEX = "https://www.ea.com/games/apex-legends/news"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def get_soup(url: str) -> BeautifulSoup:
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.raise_for_status()
    return BeautifulSoup(r.text, "lxml")

def find_latest_patch_notes_url() -> tuple[str, str]:
    soup = get_soup(EA_NEWS_INDEX)
    for a in soup.find_all("a", href=True):
        title = a.get_text(strip=True)
        if title and "patch notes" in title.lower():
            return title, urljoin("https://www.ea.com", a["href"])
    raise RuntimeError("No patch notes link found.")

def extract_article_text(article_url: str) -> str:
    soup = get_soup(article_url)
    for tag in soup(["script","style","noscript","nav","aside","footer","header"]):
        tag.decompose()
    container = soup.find("div", class_=re.compile(r"(article|rich).*body", re.I)) or \
                soup.find("section", class_=re.compile(r"(article|rich).*body", re.I)) or \
                soup.find("article") or soup.find("main") or soup
    blocks = []
    for el in container.find_all(["h1","h2","h3","h4","p","li"]):
        txt = el.get_text(" ", strip=True)
        if not txt: continue
        blocks.append(txt if el.name not in {"li"} else f"- {txt}")
    return "\n".join(blocks).strip()

def main():
    title, url = find_latest_patch_notes_url()
    text = extract_article_text(url)
    with open("latest_patch_notes.txt", "w", encoding="utf-8") as f:
        f.write(f"{title}\n{url}\n\n{text}\n")
    print(f"Saved patch notes: {title}\n{url}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(1)
