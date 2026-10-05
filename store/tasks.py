from celery import shared_task
import requests, time
from bs4 import BeautifulSoup
from store.models.product import Products

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

@shared_task
def fetch_latest_mobiles():
    url = "https://www.gsmarena.com/"
    res = requests.get(url, headers=HEADERS, timeout=20)
    soup = BeautifulSoup(res.text, "lxml")

    phones = soup.select(".makers a")[:10]  # ONLY latest 10

    for phone in phones:
        name = phone.text.strip()
        link = "https://www.gsmarena.com/" + phone["href"]

        product, created = Products.objects.get_or_create(
            name=name,
            defaults={
                "price": 0,
                "image": "",
                "category_id": 1,  # Mobiles
                "is_latest": True
            }
        )

        time.sleep(2)  # anti-ban
