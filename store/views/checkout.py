import secrets

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect

from store.models.product import Products
from store.models.address import SavedAddress


OTP_EXPIRY_SECONDS = 300


@login_required
def checkout(request):

    # -----------------------------------------
    # FIND OUT IF THIS IS "BUY NOW"
    # -----------------------------------------
    buy_now_id = request.GET.get("buy_now")

    if not buy_now_id:
        buy_now_id = request.session.get("buy_now")

    cart_items = []
    total = 0

    # -----------------------------------------
    # BUY NOW
    # -----------------------------------------
    if buy_now_id:

        request.session["buy_now"] = str(buy_now_id)

        product = Products.objects.filter(
            id=buy_now_id
        ).first()

        if not product:
            return redirect("store")

        quantity = 1
        subtotal = product.price * quantity

        cart_items = [{
            "product": product,
            "quantity": quantity,
            "subtotal": subtotal,
        }]

        total = subtotal

    # -----------------------------------------
    # NORMAL CART
    # -----------------------------------------
    else:

        request.session.pop("buy_now", None)

        cart = request.session.get("cart", {})

        products = Products.objects.filter(
            id__in=cart.keys()
        )

        for product in products:

            quantity = cart.get(
                str(product.id),
                0
            )

            if quantity <= 0:
                continue

            subtotal = product.price * quantity

            total += subtotal

            cart_items.append({
                "product": product,
                "quantity": quantity,
                "subtotal": subtotal,
            })

    saved_addresses = SavedAddress.objects.filter(
        user=request.user
    )

    # -----------------------------------------
    # USER SUBMITS CHECKOUT
    # -----------------------------------------
    if request.method == "POST":

        checkout_data = {
            "full_name": request.POST.get(
                "full_name",
                ""
            ).strip(),

            "phone": request.POST.get(
                "phone",
                ""
            ).strip(),

            "address": request.POST.get(
                "address",
                ""
            ).strip(),

            "pincode": request.POST.get(
                "pincode",
                ""
            ).strip(),

            "mode": (
                "buy_now"
                if buy_now_id
                else "cart"
            ),
        }

        # -------------------------------------
        # SAVE THE CORRECT SESSION KEY
        # -------------------------------------
        if buy_now_id:
            request.session[
                "buy_now_checkout_data"
            ] = checkout_data
        else:
            request.session[
                "checkout_data"
            ] = checkout_data

        # -------------------------------------
        # MAKE A SECURE 6 DIGIT OTP
        # -------------------------------------
        otp = str(
            secrets.randbelow(900000) + 100000
        )

        request.session["otp"] = otp
        request.session["otp_time"] = (
            __import__("time").time()
        )

        request.session.modified = True

        # -------------------------------------
        # ONLY SEND OTP TO LOGGED-IN USER
        # -------------------------------------
        email = (
            request.user.email
            or ""
        ).strip().lower()

        if not email:
            return render(
                request,
                "store/checkout.html",
                {
                    "cart_items": cart_items,
                    "total": total,
                    "saved_addresses": saved_addresses,
                    "is_buy_now": bool(buy_now_id),
                    "error": (
                        "Your account does not have "
                        "an email address. Please "
                        "complete your account first."
                    ),
                }
            )

        # -------------------------------------
        # SEND OTP BY EMAIL
        # -------------------------------------
        send_mail(
            subject="Your E-Commerce Order OTP",
            message=(
                "Your order verification OTP is: "
                f"{otp}\n\n"
                "This OTP is valid for 5 minutes.\n\n"
                "Do not share this OTP with anyone."
            ),
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        # IMPORTANT:
        # OTP is NOT printed to console.
        # OTP is NOT returned to browser.

        return redirect("verify_otp")

    return render(
        request,
        "store/checkout.html",
        {
            "cart_items": cart_items,
            "total": total,
            "saved_addresses": saved_addresses,
            "is_buy_now": bool(buy_now_id),
        }
    )