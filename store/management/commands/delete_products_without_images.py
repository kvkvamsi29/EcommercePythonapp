from django.core.management.base import BaseCommand
from django.db import connection
from store.models.product import Products


INVALID_VALUES = {"", "null", "none", "undefined", "placeholder", "no-image"}


class Command(BaseCommand):
    help = "Delete products without images (clears wishlist FK safely)"

    def handle(self, *args, **kwargs):
        deleted = 0
        kept = 0

        for product in Products.objects.all():
            image_str = str(product.image).strip().lower() if product.image else ""

            if (
                not image_str
                or any(bad in image_str for bad in INVALID_VALUES)
                or image_str.endswith("/")
                or "." not in image_str
            ):
                self.stdout.write(f"🗑️ Deleting {product.name}")

                # Delete wishlist references FIRST
                with connection.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM store_wishlist WHERE product_id = %s",
                        [product.id],
                    )

                # Now delete product
                Products.objects.filter(id=product.id).delete()
                deleted += 1
            else:
                kept += 1

        self.stdout.write(self.style.SUCCESS(
            f"DONE — {deleted} deleted, {kept} kept"
        ))
