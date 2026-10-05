from store.models.customer import Customer



def logged_in_user(request):
    customer_id = request.session.get("customer")
    if customer_id:
        try:
            customer = Customer.objects.get(id=customer_id)
            return {"logged_user": customer}
        except Customer.DoesNotExist:
            pass
    return {}

def wishlist_count(request):
    wishlist = request.session.get("wishlist", [])
    return {
        "wishlist_count": len(wishlist),
        "wishlist_ids": wishlist,
    }
def cart_count(request):
    cart = request.session.get("cart", {})
    return {
        "cart_count": sum(cart.values())
    }
def cart_product_ids(request):
    cart = request.session.get("cart", {})
    return {
        "cart_product_ids": list(map(int, cart.keys()))
    }
