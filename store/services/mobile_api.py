import requests
from django.conf import settings

BASE_URL = ""

HEADERS = {
    "X-RapidAPI-Key": settings.RAPIDAPI_KEY,
    "X-RapidAPI-Host": "mobile-phone-specs-database.p.rapidapi.com",
}

def get_brands():
    url = f"{BASE_URL}/all-brands"
    return requests.get(url, headers=HEADERS).json()

def get_phones_by_brand(brand_name):
    url = f"{BASE_URL}/get-models-by-brandname/{brand_name}"
    res = requests.get(url, headers=HEADERS)

   
    return res.json()


def get_phone_details(phone_name):
    url = f"{BASE_URL}/get-specifications/{phone_name}"
    return requests.get(url, headers=HEADERS).json()
