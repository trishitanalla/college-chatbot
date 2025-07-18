import requests
from bs4 import BeautifulSoup
import json

def scrape_site(base_url="https://srivasaviengg.ac.in/"):
    visited, to_visit, output = set(), [base_url], []
    while to_visit:
        url = to_visit.pop()
        if url in visited: continue
        visited.add(url)
        resp = requests.get(url)
        if resp.status_code != 200: continue
        soup = BeautifulSoup(resp.text, "html.parser")
        text = soup.get_text(separator="\n", strip=True)
        output.append({"url": url, "text": text})
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if href.startswith("/"):
                href = base_url.rstrip("/") + href
            if href.startswith(base_url) and href not in visited:
                to_visit.append(href)
    with open("scraped.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"Scraped {len(output)} pages.")

if __name__ == "__main__":
    scrape_site()
