from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout

from store.models.cart import load_cart_from_db


class Login(View):

    def get(self, request):
        return render(request, "login.html")

    def post(self, request):

        username = request.POST.get("username")
        password = request.POST.get("password")

        if not username or not password:
            return render(request, "login.html", {
                "error": "Username and password are required"
            })

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return render(request, "login.html", {
                "error": "Invalid username or password"
            })

        # ============================
        # LOGIN
        # ============================
        dj_login(request, user)

        # ============================
        # EXISTING USER WITHOUT EMAIL
        # ============================
        if not user.email:

            return redirect("complete_account")

        # ============================
        # AUTO-ADD PENDING CART PRODUCT
        # ============================
        pending_product = request.session.pop(
            "pending_cart_product",
            None
        )

        if pending_product:

            cart = request.session.get("cart", {})

            pid = str(pending_product)

            cart[pid] = cart.get(pid, 0) + 1

            request.session["cart"] = cart

            request.session.modified = True

        # ============================
        # LOAD CART
        # ============================
        load_cart_from_db(request)

        next_url = request.GET.get("next")

        return redirect(next_url or "store")