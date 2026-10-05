def normalize_mobile(api_data):
    return {
        "name": api_data.get("model"),
        "price": 50000,  # estimated or fetched separately
        "description": api_data.get("description", ""),
        "image": api_data.get("image"),
        "specifications": {
            "Display": api_data.get("display"),
            "Processor": api_data.get("chipset"),
            "RAM": api_data.get("ram"),
            "Battery": api_data.get("battery"),
            "Camera": api_data.get("camera"),
            "OS": api_data.get("os")
        }
    }
