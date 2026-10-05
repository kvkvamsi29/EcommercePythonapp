import threading
from store.services.device_scraper import scrape_gsmarena
from store.services.feature_generator import generate_features_from_specs

def scrape_async(product):
    def task():
        specs = scrape_gsmarena(product.name)
        if specs:
            product.specifications = specs
            product.features = generate_features_from_specs(specs)
            product.save()

    threading.Thread(target=task).start()
