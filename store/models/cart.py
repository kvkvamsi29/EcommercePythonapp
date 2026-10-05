from django.db import models
from django.contrib.auth.models import User
from .product import Products


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"


# ---------------------------
# SAVE SESSION CART TO DB
# ---------------------------
def save_session_cart_to_db(request):
    if not request.user.is_authenticated:
        return

    from .cart import CartItem
    from .product import Products

    cart = request.session.get("cart", {})
    CartItem.objects.filter(user=request.user).delete()
    for product_id, qty in cart.items():
        product = Products.objects.filter(id=product_id).first()
        if product:
             CartItem.objects.create(
        user=request.user,
        product=product,
        quantity=qty
    )


# ---------------------------
# LOAD CART FROM DB TO SESSION
# ---------------------------
def load_cart_from_db(request):
    if not request.user.is_authenticated:
        return

    from .cart import CartItem

    cart_items = CartItem.objects.filter(user=request.user)

    cart = {}
    for item in cart_items:
        cart[str(item.product.id)] = item.quantity

    request.session["cart"] = cart
    request.session.modified = True
