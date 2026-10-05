from django.core.management.base import BaseCommand
from store.services.product_loader import load_products_from_api

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        load_products_from_api()
        self.stdout.write("Products loaded from API")
