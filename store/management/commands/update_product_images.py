import json
from django.core.management.base import BaseCommand
from store.models.product import Products


class Command(BaseCommand):
    help = "Manually update image URLs for products with missing images"

    def handle(self, *args, **kwargs):
        path = "store/management/commands/image_updates.json"

        with open(path, "r", encoding="utf-8") as f:
            updates = json.load(f)

        updated = 0
        skipped = 0

        for item in updates:
            model = item.get("model")
            image_url = item.get("image_url")

            if not model or not image_url:
                skipped += 1
                continue

            product = Products.objects.filter(name=model).first()

            if not product:
                self.stdout.write(f"❌ Product not found: {model}")
                skipped += 1
                continue

            # Only update if image is missing
            if product.image:
                self.stdout.write(f"⚠ Image already exists: {model}")
                skipped += 1
                continue

            product.image = image_url
            product.save()

            updated += 1
            self.stdout.write(f"✅ Updated image: {model}")

        self.stdout.write(self.style.SUCCESS(
            f"\nDONE ✅  Updated: {updated}, Skipped: {skipped}"
        ))
