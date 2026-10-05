from store.models.product import Products
from store.services.mobilespecs_api import search_phone, get_phone_details
from store.services.spec_normalizer import normalize_specs
from store.services.feature_generator import generate_features_from_specs
from store.services.device_classifier import detect_product_type


def live_import_product(product):
    # Skip if already enriched
    if product.specifications:
        return False

    phones = search_phone(product.name)
    if not phones:
        return False

    slug = phones[0]["slug"]
    details = get_phone_details(slug)

    specs = normalize_specs(details.get("specifications", []))
    features = generate_features_from_specs(specs)

    product.specifications = specs
    product.features = features
    product.product_type = detect_product_type(product.name)
    product.is_latest = True
    product.save()

    return True
