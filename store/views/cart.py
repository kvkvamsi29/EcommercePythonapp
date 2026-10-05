from django.shortcuts import render, redirect
from store.models.product import Products

from django.http import JsonResponse
from store.models.product import Products
from django.contrib.auth.decorators import login_required

from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect
from store.models.product import Products


from django.http import JsonResponse

from django.http import JsonResponse
from django.shortcuts import redirect

def add_to_cart(request, product_id):
    action = request.GET.get("action", "add")

    cart = request.session.get("cart", {})
    pid = str(product_id)

    if action == "add":
        cart[pid] = cart.get(pid, 0) + 1

    elif action == "increase":
        cart[pid] = cart.get(pid, 1) + 1

    elif action == "decrease":
        if cart.get(pid, 1) > 1:
            cart[pid] -= 1
        else:
            cart.pop(pid, None)

    elif action == "remove":
        cart.pop(pid, None)

    request.session["cart"] = cart
    request.session.modified = True

    cart_count = sum(cart.values())

    # ✅ AJAX request → return JSON (store page)
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({
            "status": "ok",
            "count": cart_count
        })

    # ✅ NORMAL request → stay on same page (cart page)
    return redirect(request.META.get("HTTP_REFERER", "cart"))



def cart(request):
    cart = request.session.get("cart", {})
    product_ids = cart.keys()

    products = Products.objects.filter(id__in=product_ids)

    cart_items = []
    total = 0

    for product in products:
        qty = cart[str(product.id)]
        subtotal = product.price * qty
        total += subtotal

        cart_items.append({
            "product": product,
            "quantity": qty,
            "subtotal": subtotal
        })

    return render(request, "store/cart.html", {
        "cart_items": cart_items,
        "total": total
    })
    
    





@csrf_exempt   # TEMPORARY (we’ll harden later)
@require_POST
# def api_cart_add(request, product_id):
#     qty = int(request.POST.get("qty", 1))
#     cart = request.session.get("cart", {})
#     pid = str(product_id)

#     cart[pid] = cart.get(pid, 0) + qty
#     request.session["cart"] = cart
#     request.session.modified = True

#     return JsonResponse({
#         "status": "added",
#         "cart_count": sum(cart.values())
#     })

@csrf_exempt
@require_POST
def api_cart_update(request, product_id):
    action = request.POST.get("action")
    cart = request.session.get("cart", {})
    pid = str(product_id)

    if pid not in cart:
        return JsonResponse({"status": "invalid"}, status=400)

    if action == "increase":
        cart[pid] += 1
    elif action == "decrease":
        if cart[pid] > 1:
            cart[pid] -= 1
        else:
            cart.pop(pid)
    elif action == "remove":
        cart.pop(pid)

    request.session["cart"] = cart
    request.session.modified = True

    return JsonResponse({
        "status": "updated",
        "cart_count": sum(cart.values())
    })


def cart_count(request):
    cart = request.session.get("cart", {})
    count = sum(cart.values())
    return JsonResponse({"count": count})

def cart_count_api(request):
    cart = request.session.get("cart", {})
    return JsonResponse({
        "count": sum(cart.values())
    })