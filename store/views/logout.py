from django.contrib.auth import logout
from django.shortcuts import redirect
from store.models.cart import save_session_cart_to_db


def custom_logout(request):
    # Save cart before clearing session
    save_session_cart_to_db(request)

    # Logout user (Django clears session here)
    logout(request)

    return redirect("login")
