import json
from django.core.management.base import BaseCommand
from store.models.product import Products


class Command(BaseCommand):
    help = "Update laptop image URLs using JSON mapping"

    def handle(self, *args, **kwargs):

        with open("laptop_image_updates.json", "r", encoding="utf-8") as f:
            data = json.load(f)

        updated = 0
        not_found = 0

        for item in data:
            name_key = item["name_contains"].lower()
            image_url = item["image"]

            # Loose matching
            products = Products.objects.filter(name__icontains=name_key)

            if not products.exists():
                self.stdout.write(self.style.WARNING(f"❌ Not found: {name_key}"))
                not_found += 1
                continue

            for product in products:
                old = product.image

                product.image = image_url
                product.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"✔ Updated {product.name}\n"
                        f"   OLD: {old}\n"
                        f"   NEW: {image_url}\n"
                    )
                )

                updated += 1

        self.stdout.write(self.style.SUCCESS(
            f"\nDONE 🚀\nUpdated: {updated}\nNot found: {not_found}"
        ))
