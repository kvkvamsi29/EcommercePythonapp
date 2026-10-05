import random

def generate_specs(product_name: str):
    name = product_name.lower()

    # ---------- MOBILE SPECS ----------
    if any(x in name for x in ["iphone", "galaxy", "redmi", "realme", "pixel", "oneplus", "moto"]):
        specs = {
            "Technology": "GSM / LTE / 5G",
            "Display": random.choice([
                "6.1-inch AMOLED 120Hz",
                "6.5-inch OLED 120Hz",
                "6.7-inch AMOLED 120Hz"
            ]),
            "Processor": random.choice([
                "Snapdragon 8 Gen 2",
                "Snapdragon 7+ Gen 2",
                "MediaTek Dimensity 8100",
                "Apple A16 Bionic"
            ]),
            "RAM": random.choice(["6GB", "8GB", "12GB"]),
            "Storage": random.choice(["128GB", "256GB", "512GB"]),
            "Battery": random.choice(["4500 mAh", "5000 mAh"]),
            "Rear Camera": random.choice([
                "50MP + 12MP + 10MP",
                "48MP + 12MP",
                "64MP + 8MP + 2MP"
            ]),
            "Front Camera": random.choice(["12MP", "16MP", "32MP"]),
            "OS": "Android 13" if "iphone" not in name else "iOS 16"
        }
        return specs

    # ---------- TABLET SPECS ----------
    if any(x in name for x in ["ipad", "tablet", "tab", "surface"]):
        return {
            "Display": "11-inch IPS LCD",
            "Processor": "Snapdragon 870 / Apple M1",
            "RAM": "8GB",
            "Storage": "256GB",
            "Battery": "8000 mAh",
            "OS": "Android / iPadOS",
            "Connectivity": "Wi-Fi / LTE"
        }

    # ---------- LAPTOP SPECS ----------
    if any(x in name for x in ["macbook", "laptop", "dell", "hp", "lenovo", "asus"]):
        return {
            "Display": "15.6-inch Full HD",
            "Processor": random.choice([
                "Intel Core i5 12th Gen",
                "Intel Core i7 12th Gen",
                "Apple M1"
            ]),
            "RAM": random.choice(["8GB", "16GB"]),
            "Storage": random.choice(["512GB SSD", "1TB SSD"]),
            "Graphics": "Integrated / Dedicated",
            "OS": "Windows 11 / macOS"
        }

    return None
