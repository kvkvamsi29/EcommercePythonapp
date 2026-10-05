from django.views import View
from django.shortcuts import render, get_object_or_404
from store.models.product import Products
import ast
from django.shortcuts import render, get_object_or_404
from store.models.product import Products
from store.models.product import Products
from store.services.live_import import live_import_product

from store.services.mobile_api import get_phone_details
from store.services.async_tasks import scrape_async

class ProductDetail(View):
    def get(self, request, id):
        product = get_object_or_404(Products, id=id)

        if not product.specifications:
            scrape_async(product)

        return render(request, 'product_detail.html', {
            'product': product
        })
   





from django.shortcuts import get_object_or_404
from store.models.product import Products


def product_detail(request, id):
    product = get_object_or_404(Products, id=id)

    api_specs = None
    if product.api_phone_id:
        api_specs = get_phone_details(product.api_phone_id)

    context = {
        "product": product,
        "api_specs": api_specs
    }

    return render(request, "store/product_detail.html", context)
