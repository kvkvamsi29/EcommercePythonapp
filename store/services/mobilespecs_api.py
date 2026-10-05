import requests

BASE_URL = "https://api-mobilespecs.azharimm.dev/v2"

def search_phone(query):
    url = f"{BASE_URL}/search?query={query}"
    res = requests.get(url, timeout=15)
    res.raise_for_status()
    return res.json().get("data", {}).get("phones", [])


def get_phone_details(slug):
    url = f"{BASE_URL}/{slug}"
    res = requests.get(url, timeout=15)
    res.raise_for_status()
    return res.json().get("data", {})
