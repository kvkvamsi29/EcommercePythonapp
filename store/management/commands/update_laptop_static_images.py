from django.core.management.base import BaseCommand
from store.models.product import Products
import json


class Command(BaseCommand):
    help = "Update laptop images from static files"

    def handle(self, *args, **kwargs):
        with open("laptop_static_images.json", "r", encoding="utf-8") as f:
            mappings = json.load(f)

        updated = 0

        laptops = Products.objects.filter(product_type="laptop")

        for laptop in laptops:
            name_lower = laptop.name.lower()

            for item in mappings:
                if item["name_contains"] in name_lower:
                    laptop.image = item["image"]
                    laptop.save(update_fields=["image"])
                    updated += 1

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"🖼 Updated image → {laptop.name}"
                        )
                    )
                    break

        self.stdout.write(self.style.SUCCESS(
            f"\nDONE ✅ Laptop images updated: {updated}"
        ))
