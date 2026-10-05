import json
from django.core.management.base import BaseCommand
from store.services.api_products import (
    fetch_mobile_list,
    fetch_laptop_list,
    fetch_tablet_list,
)

OUTPUT_FILE = "all_devices_full.json"


class Command(BaseCommand):
    help = "Build unified JSON for mobiles, laptops, and tablets"

    def handle(self, *args, **kwargs):
        devices = []

        # ===============================
        # 1. LOAD EXISTING MOBILE JSON
        # ===============================
        try:
            with open("strict_100_real_full_specs.json", "r", encoding="utf-8") as f:
                mobiles = json.load(f)

            for m in mobiles:
                m["device_type"] = "mobile"
                devices.append(m)

            self.stdout.write(f"✔ Loaded {len(mobiles)} mobiles from JSON")

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed loading mobiles JSON: {e}"))

        # ===============================
        # 2. LOAD LAPTOPS FROM SERVICES
        # ===============================
        for l in fetch_laptop_list():
            devices.append({
                "model": l["name"],
                "price": l["price"],
                "features": [l["description"]],
                "image_url": l["image"],
                "device_type": "laptop",
                "specifications": l,
            })

        self.stdout.write(f"✔ Loaded laptops")

        # ===============================
        # 3. LOAD TABLETS FROM SERVICES
        # ===============================
        for t in fetch_tablet_list():
            devices.append({
                "model": t["name"],
                "price": t["price"],
                "features": [t["description"]],
                "image_url": t["image"],
                "device_type": "tablet",
                "specifications": t,
            })

        self.stdout.write(f"✔ Loaded tablets")

        # ===============================
        # 4. WRITE FINAL JSON
        # ===============================
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f"\nDONE ✅  Unified JSON created → {OUTPUT_FILE}\n"
            f"Total devices: {len(devices)}"
        ))
