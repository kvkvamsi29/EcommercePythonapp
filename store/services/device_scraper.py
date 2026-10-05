import requests
from bs4 import BeautifulSoup

HEADERS = {"User-Agent": "Mozilla/5.0"}

def scrape_gsmarena(device_name):
    url = f"https://www.gsmarena.com/results.php3?sQuickSearch=yes&sName={device_name.replace(' ', '+')}"
    r = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(r.text, "html.parser")

    link = soup.select_one(".makers a")
    if not link:
        return None

    page = requests.get("https://www.gsmarena.com/" + link["href"], headers=HEADERS)
    soup = BeautifulSoup(page.text, "html.parser")

    specs = {}
    for row in soup.select("table tr"):
        k = row.select_one(".ttl")
        v = row.select_one(".nfo")
        if k and v:
            specs[k.text.strip()] = v.text.strip()

    return specs
