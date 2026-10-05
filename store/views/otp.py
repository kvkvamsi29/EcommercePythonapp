import secrets
import time
import uuid

from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from store.models.order import Order
from store.models.customer import Customer
from store.models.product import Products


OTP_EXPIRY_SECONDS = 300


def generate_otp():
    return str(
        secrets.randbelow(900000) + 100000
    )


@login_required
def verify_otp(request):

    otp = request.session.get("otp")
    otp_time = request.session.get("otp_time")

    # -----------------------------------------
    # OTP DOES NOT EXIST
    # -----------------------------------------
    if not otp or not otp_time:
        return render(
            request,
            "store/verify_otp.html",
            {
                "error": (
                    "OTP expired. "
                    "Please request a new OTP."
                )
            }
        )

    # -----------------------------------------
    # CHECK OTP EXPIRATION
    # -----------------------------------------
    if time.time() - float(otp_time) > OTP_EXPIRY_SECONDS:

        request.session.pop("otp", None)
        request.session.pop("otp_time", None)

        return render(
            request,
            "store/verify_otp.html",
            {
                "error": (
                    "OTP expired. "
                    "Please request a new OTP."
                )
            }
        )

    # -----------------------------------------
    # VERIFY USER ENTERED OTP
    # -----------------------------------------
    if request.method == "POST":

        entered_otp = request.POST.get(
            "otp",
            ""
        ).strip()

        if not entered_otp.isdigit() or len(entered_otp) != 6:

            return render(
                request,
                "store/verify_otp.html",
                {
                    "error": "Enter the 6-digit OTP."
                }
            )

        if not secrets.compare_digest(
            entered_otp,
            str(otp)
        ):

            return render(
                request,
                "store/verify_otp.html",
                {
                    "error": "Invalid OTP. Try again."
                }
            )

        # -------------------------------------
        # DETERMINE CART MODE
        # -------------------------------------
        buy_now_product_id = request.session.get(
            "buy_now"
        )

        is_buy_now = bool(
            buy_now_product_id
        )

        if is_buy_now:

            cart = {
                str(buy_now_product_id): 1
            }

            checkout_data = request.session.get(
                "buy_now_checkout_data",
                {}
            )

        else:

            cart = request.session.get(
                "cart",
                {}
            )

            checkout_data = request.session.get(
                "checkout_data",
                {}
            )

        if not cart:

            return render(
                request,
                "store/verify_otp.html",
                {
                    "error": (
                        "Your cart is empty."
                    )
                }
            )

        # -------------------------------------
        # USE LOGGED-IN ACCOUNT EMAIL
        # -------------------------------------
        customer_email = (
            request.user.email
            or ""
        ).strip().lower()

        if not customer_email:

            return render(
                request,
                "store/verify_otp.html",
                {
                    "error": (
                        "Your account does not "
                        "have an email address."
                    )
                }
            )

        # -------------------------------------
        # FIND CUSTOMER BY EMAIL
        # -------------------------------------
        customer = Customer.objects.filter(
            email__iexact=customer_email
        ).order_by("-id").first()

        customer_name = checkout_data.get(
            "full_name",
            ""
        ).strip()

        customer_phone = checkout_data.get(
            "phone",
            ""
        ).strip()

        name_parts = customer_name.split()

        first_name = (
            name_parts[0]
            if name_parts
            else "Customer"
        )

        last_name = (
            " ".join(name_parts[1:])
            if len(name_parts) > 1
            else ""
        )

        if not customer:

            customer = Customer.objects.create(
                first_name=first_name,
                last_name=last_name,
                phone=customer_phone,
                email=customer_email,
                password="",
            )

        else:

            # Keep the customer information updated.
            customer.first_name = first_name
            customer.last_name = last_name
            customer.phone = customer_phone
            customer.email = customer_email

            customer.save(
                update_fields=[
                    "first_name",
                    "last_name",
                    "phone",
                    "email",
                ]
            )

        # -------------------------------------
        # GET PRODUCTS
        # -------------------------------------
        if is_buy_now:

            products = Products.objects.filter(
                id=buy_now_product_id
            )

        else:

            product_ids = [
                int(product_id)
                for product_id in cart.keys()
            ]

            products = Products.objects.filter(
                id__in=product_ids
            )

        if not products.exists():

            return render(
                request,
                "store/verify_otp.html",
                {
                    "error": (
                        "Products not found."
                    )
                }
            )

        # -------------------------------------
        # CREATE ONE ORDER GROUP
        # -------------------------------------
        order_group_id = str(
            uuid.uuid4()
        )[:8]

        for product in products:

            quantity = cart.get(
                str(product.id),
                0
            )

            if quantity <= 0:
                continue

            Order.objects.create(
                customer=customer,
                product=product,
                quantity=quantity,
                price=product.price * quantity,
                address=checkout_data.get(
                    "address",
                    ""
                ),
                phone=checkout_data.get(
                    "phone",
                    ""
                ),
                status=0,
                order_id=order_group_id,
            )

        # -------------------------------------
        # CLEAN UP SESSION
        # -------------------------------------
        if not is_buy_now:

            request.session["cart"] = {}

        request.session.pop(
            "buy_now",
            None
        )

        request.session.pop(
            "buy_now_checkout_data",
            None
        )

        request.session.pop(
            "checkout_data",
            None
        )

        request.session.pop(
            "otp",
            None
        )

        request.session.pop(
            "otp_time",
            None
        )

        request.session[
            "last_order_id"
        ] = order_group_id

        request.session.modified = True

        return redirect("payment")

    return render(
        request,
        "store/verify_otp.html"
    )


@login_required
@require_POST
def send_otp(request):

    email = (
        request.user.email
        or ""
    ).strip().lower()

    if not email:

        return JsonResponse(
            {
                "status": "error",
                "message": (
                    "Your account does not "
                    "have an email address."
                ),
            },
            status=400
        )

    otp = generate_otp()

    request.session["otp"] = otp
    request.session["otp_time"] = time.time()
    request.session.modified = True

    send_mail(
        subject="Your E-Commerce Order OTP",
        message=(
            "Your new order verification OTP is: "
            f"{otp}\n\n"
            "This OTP is valid for 5 minutes.\n\n"
            "Do not share this OTP with anyone."
        ),
        from_email=None,
        recipient_list=[email],
        fail_silently=False,
    )

    # Notice:
    # We return only "ok".
    # We NEVER return the OTP itself.

    return JsonResponse(
        {
            "status": "ok"
        }
    ) 