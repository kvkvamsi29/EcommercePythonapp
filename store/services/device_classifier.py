def detect_product_type(name):
    n = name.lower()

    if any(x in n for x in ["iphone", "galaxy", "pixel", "realme", "redmi", "oneplus"]):
        return "mobile"

    if any(x in n for x in ["ipad", "tablet", "tab"]):
        return "tablet"

    if any(x in n for x in ["macbook", "laptop", "dell", "hp", "lenovo", "asus"]):
        return "laptop"

    return "mobile"
