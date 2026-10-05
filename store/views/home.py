from django.shortcuts import render
from django.db.models import Q
from store.models.product import Products
from store.models.category import Category


def store(request):
    search_query = request.GET.get("q", "").strip()
    product_type = request.GET.get("product_type")
    selected_category = product_type

    products = Products.objects.all()

    # -------------------------------
    # SEARCH (WORKING)
    # -------------------------------
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    # -------------------------------
    # ✅ CATEGORY FILTER (REAL FIX)
    # -------------------------------
    CATEGORY_MAP = {
        "mobile": "mobile",
        "laptop": "laptop",
        "tablet": "tablet",
    }

    if product_type in CATEGORY_MAP:
        products = products.filter(
            category__name__icontains=CATEGORY_MAP[product_type]
        )

    # -------------------------------
    # CART IDS
    # -------------------------------
    cart = request.session.get("cart", {})
    cart_product_ids = list(map(int, cart.keys()))

    context = {
        "products": products,
        "categories": Category.objects.all(),
        "cart_product_ids": cart_product_ids,
        "search_query": search_query,
        "selected_category": selected_category,
    }

    return render(request, "store/store.html", context)
