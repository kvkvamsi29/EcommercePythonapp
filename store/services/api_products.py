import requests

def fetch_mobile_list():
    # Example API-style response (simulate / replace with RapidAPI)
    return [
        {
            "name": "iPhone 14 Pro",
            "price": 129999,
            "image": "https://fdn2.gsmarena.com/vv/pics/apple/apple-iphone-14-pro-1.jpg",
            "description": "Apple flagship smartphone"
        },
        {
            "name": "Samsung Galaxy S23 Ultra",
            "price": 124999,
            "image": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-s23-ultra-1.jpg",
            "description": "Premium Android smartphone"
        }
    ]


def fetch_laptop_list():
    return [
        {
            "name": "MacBook Air M2",
            "price": 114999,
            "image": "https://m.media-amazon.com/images/I/71f5Eu5lJSL._SX679_.jpg",
            "description": "Ultra thin Apple laptop"
        }
    ]


def fetch_tablet_list():
    return [
        {
            "name": "Samsung Galaxy Tab S8",
            "price": 69999,
            "image": "https://fdn2.gsmarena.com/vv/pics/samsung/samsung-galaxy-tab-s8-ultra-1.jpg",
            "description": "Powerful Android tablet"
        }
    ]
