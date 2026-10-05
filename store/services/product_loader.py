from store.models.product import Products
from store.models.category import Category




from store.models.product import Products
from store.models.category import Category
from store.services.api_products import (
    fetch_mobile_list,
    fetch_laptop_list,
    fetch_tablet_list
)

def load_products_from_api():
    mobiles = Category.objects.get(name__iexact="Mobiles")
    laptops = Category.objects.get(name__iexact="Laptops")
    tablets = Category.objects.get(name__iexact="Tablets")

    sources = [
        (fetch_mobile_list(), mobiles),
        (fetch_laptop_list(), laptops),
        (fetch_tablet_list(), tablets)
    ]

    for items, category in sources:
        for item in items:
            Products.objects.get_or_create(
                name=item["name"],
                defaults={
                    "price": item["price"],
                    "image": item["image"],
                    "description": item["description"],
                    "category": category,
                    
                }
            )



def load_sample_products():
    mobiles = Category.objects.get(name__iexact="Mobiles")
    laptops = Category.objects.get(name__iexact="Laptops")
    tablets = Category.objects.get(name__iexact="Tablets")

    data = [
        # ---------- MOBILES ----------
        {
            "name": "iPhone 14 Pro",
            "price": 129999,
            "category": mobiles,
            "image": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-14-pro-1.jpg",
            "description": "Apple flagship smartphone"
        },
        {
            "name": "Samsung Galaxy S23 Ultra",
            "price": 124999,
            "category": mobiles,
            "image": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s23-ultra-1.jpg",
            "description": "Premium Android smartphone"
        },

        # ---------- LAPTOPS ----------
        {
            "name": "MacBook Air M2",
            "price": 114999,
            "category": laptops,
            "image": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SX679_.jpg",
            "description": "Ultra thin Apple laptop"
        },

        # ---------- TABLETS ----------
        {
            "name": "Samsung Galaxy Tab S8",
            "price": 69999,
            "category": tablets,
            "image": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-tab-s8-ultra-1.jpg",
            "description": "Powerful Android tablet"
        }
    ]

    for item in data:
        Products.objects.get_or_create(
            name=item["name"],
            defaults=item
        )
