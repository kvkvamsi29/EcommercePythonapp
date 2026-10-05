import json
from django.core.management.base import BaseCommand

# ⬇️ IMPORT FROM YOUR PROJECT (ADJUST PATH IF NEEDED)
from store.services.api_products import (
    fetch_laptop_list,
    fetch_tablet_list,
)

OUTPUT_FILE = "laptops_tablets_from_project.json"


class Command(BaseCommand):
    help = "Extract all laptops & tablets from project code into JSON"

    def handle(self, *args, **kwargs):
        devices = []

        # ======================
        # LAPTOPS
        # ======================
        laptops = fetch_laptop_list()
        for item in laptops:
            devices.append({
                "model": item.get("name"),
                "price": item.get("price"),
                "features": [item.get("description")] if item.get("description") else [],
                "image_url": item.get("image"),
                "device_type": "laptop",
                "specifications": item,
                "source": "project_code"
            })

        self.stdout.write(f"✔ Extracted {len(laptops)} laptops")

        # ======================
        # TABLETS
        # ======================
        tablets = fetch_tablet_list()
        for item in tablets:
            devices.append({
                "model": item.get("name"),
                "price": item.get("price"),
                "features": [item.get("description")] if item.get("description") else [],
                "image_url": item.get("image"),
                "device_type": "tablet",
                "specifications": item,
                "source": "project_code"
            })

        self.stdout.write(f"✔ Extracted {len(tablets)} tablets")

        # ======================
        # WRITE JSON
        # ======================
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f"\nDONE ✅ JSON created: {OUTPUT_FILE}\n"
            f"Total devices: {len(devices)}"
        ))
