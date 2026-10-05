import json
from django.core.management.base import BaseCommand
from store.models.product import Products
from store.models.category import Category


class Command(BaseCommand):
    help = "Import / Update ALL devices (phones, laptops, tablets) from JSON — SAFE MODE"

    def handle(self, *args, **kwargs):
        path = "all_devices_full.json"

        try:
            with open(path, "r", encoding="utf-8") as f:
                devices = json.load(f)
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to load JSON: {e}"))
            return

        created = 0
        updated = 0
        skipped = 0

        for item in devices:
            model_name = item.get("model")
            api_id = item.get("api_phone_id")
            image_url = item.get("image_url")

            if not model_name:
                skipped += 1
                continue

            # ============================
            # DETECT DEVICE TYPE
            # ============================
            raw_type = (
                item.get("device_type")
                or item.get("type")
                or item.get("category")
                or item.get("product_type")
                or "mobile"
            )

            raw_type = str(raw_type).lower()

            if "laptop" in raw_type:
                product_type = "laptop"
                category_name = "Laptop"
            elif "tablet" in raw_type:
                product_type = "tablet"
                category_name = "Tablet"
            else:
                product_type = "mobile"
                category_name = "Mobile"

            category, _ = Category.objects.get_or_create(name=category_name)

            # ============================
            # EXTRACT PRICE (JSON ONLY)
            # ============================
            raw_price = (
                item.get("price")
                or item.get("price_inr")
                or item.get("launch_price")
                or item.get("pricing")
                or item.get("specifications", {}).get("price")
            )

            price = None
            if raw_price:
                if isinstance(raw_price, str):
                    digits = "".join(filter(str.isdigit, raw_price))
                    price = int(digits) if digits else None
                elif isinstance(raw_price, (int, float)):
                    price = int(raw_price)

            if not price:
                price = 999  # SAFE FALLBACK

            # ============================
            # FEATURES / DESCRIPTION
            # ============================
            features = item.get("features", [])
            description = (
                ", ".join(features)
                if isinstance(features, list)
                else str(features)
            )

            # ============================
            # FIND OR CREATE PRODUCT
            # ============================
            obj = None
            if api_id:
                obj = Products.objects.filter(api_phone_id=api_id).first()

            if not obj:
                obj = Products.objects.filter(name=model_name).first()

            is_new = False
            if not obj:
                obj = Products(name=model_name)
                is_new = True

            # ============================
            # FORCE UPDATE (SAFE)
            # ============================
            obj.price = price
            obj.description = description
            obj.features = features
            obj.specifications = item
            obj.product_type = product_type
            obj.category = category
            obj.is_latest = True

            if api_id:
                obj.api_phone_id = api_id

            # NEVER overwrite image if already exists
            if image_url and not obj.image:
                obj.image = image_url

            obj.save()

            if is_new:
                created += 1
                self.stdout.write(f"➕ Created: {model_name}")
            else:
                updated += 1
                self.stdout.write(f"♻ Updated: {model_name}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDONE ✅  Created: {created} | Updated: {updated} | Skipped: {skipped}"
        ))
