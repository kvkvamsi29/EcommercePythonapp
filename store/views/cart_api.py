from django.http import JsonResponse
from store.models.product import Products

def mini_cart(request):
    cart = request.session.get("cart", {})
    product_ids = cart.keys()

    products = Products.objects.filter(id__in=product_ids)

    items = []
    total = 0

    for p in products:
        qty = cart[str(p.id)]
        subtotal = p.price * qty
        total += subtotal

        items.append({
            "name": p.name,
            "qty": qty,
            "price": float(p.price),
        })

    return JsonResponse({
        "items": items,
        "total": float(total)
    })
from django.http import JsonResponse
from store.models.product import Products

from django.http import JsonResponse
from store.models.product import Products

def api_cart_add(request, product_id):
    cart = request.session.get("cart", {})

    product_id = str(product_id)
    cart[product_id] = cart.get(product_id, 0) + 1

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({
        "status": "added",
        "product_id": product_id,
        "cart_count": sum(cart.values())
    })
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt


@require_POST
def api_cart_update(request, product_id):
    action = request.POST.get("action")
    cart = request.session.get("cart", {})
    pid = str(product_id)

    if pid not in cart:
        return JsonResponse({
            "status": "removed",
            "cart_count": sum(cart.values())
        })

    if action == "increase":
        cart[pid] += 1

    elif action == "decrease":
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            cart.pop(pid)  # ✅ ACTUAL DELETE

    elif action == "remove":
        cart.pop(pid)

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({
        "status": "updated",
        "cart_count": sum(cart.values())
    })
