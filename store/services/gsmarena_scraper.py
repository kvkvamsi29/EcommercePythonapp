import requests
from bs4 import BeautifulSoup
from store.models.product import Products

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

def fetch_latest_mobiles(limit=10):
    url = "https://www.gsmarena.com/phones.php"
    response = requests.get(url, headers=HEADERS, timeout=15)

    # DO NOT raise_for_status() to avoid hard crashes
    if response.status_code != 200:
       
        return 0

    soup = BeautifulSoup(response.text, "lxml")

    # This selector is currently stable
    phones = soup.select("div.makers a")

    count = 0
    for phone in phones:
        name = phone.text.strip()
        if not name:
            continue

        _, created = Products.objects.get_or_create(
            name=name,
            defaults={
                "price": 0,
                "image": "https://via.placeholder.com/300x300?text=Mobile",
                "category_id": 1,   # Mobiles
                "is_latest": True
            }
        )

        if created:
            count += 1

        if count >= limit:
            break

    return count
