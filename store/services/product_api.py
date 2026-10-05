import requests

RAPIDAPI_KEY = "YOUR_RAPIDAPI_KEY"

HEADERS = {
    "X-RapidAPI-Key": RAPIDAPI_KEY,
    "X-RapidAPI-Host": "mobile-phone-specs-database.p.rapidapi.com"
}

def fetch_mobile_products(brand="apple"):
    url = "https://mobile-phone-specs-database.p.rapidapi.com/gsm/get-models"
    response = requests.get(url, headers=HEADERS, params={"brand": brand})
    return response.json().get("data", [])


def fetch_mobile_specs(model_name):
    url = "https://mobile-phone-specs-database.p.rapidapi.com/gsm/get-specs"
    response = requests.get(url, headers=HEADERS, params={"model": model_name})
    return response.json()
