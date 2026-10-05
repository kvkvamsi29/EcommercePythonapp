import os
import json
import ast
from django.core.management.base import BaseCommand


PROJECT_DIR = "store"
OUTPUT_FILE = "all_devices_from_project_scan.json"

PRODUCT_KEYS = {"name", "price", "image", "description"}


class Command(BaseCommand):
    help = "Scan project files and extract all hardcoded laptops/tablets"

    def handle(self, *args, **kwargs):
        devices = []

        for root, _, files in os.walk(PROJECT_DIR):
            for file in files:
                if not file.endswith(".py"):
                    continue

                path = os.path.join(root, file)

                try:
                    with open(path, "r", encoding="utf-8") as f:
                        tree = ast.parse(f.read(), filename=path)
                except Exception:
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.Dict):
                        keys = []
                        for k in node.keys:
                            if isinstance(k, ast.Constant):
                                keys.append(str(k.value))

                        if PRODUCT_KEYS.issubset(set(keys)):
                            product = {}
                            for k, v in zip(node.keys, node.values):
                                if isinstance(k, ast.Constant):
                                    try:
                                        product[k.value] = ast.literal_eval(v)
                                    except Exception:
                                        pass

                            # Infer device type
                            name = product.get("name", "").lower()
                            if "tab" in name or "ipad" in name:
                                product["device_type"] = "tablet"
                            elif "book" in name or "laptop" in name:
                                product["device_type"] = "laptop"
                            else:
                                continue  # ignore mobiles here

                            product["source"] = path
                            devices.append(product)

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(devices, f, indent=2)

        self.stdout.write(self.style.SUCCESS(
            f"DONE ✅  Extracted {len(devices)} devices → {OUTPUT_FILE}"
        ))
