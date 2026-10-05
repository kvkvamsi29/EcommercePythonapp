import random
import time

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail


OTP_EXPIRY_SECONDS = 300  # 5 minutes


@login_required
def complete_account(request):

    # User already has an email.
    if request.user.email:
        return redirect("store")

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()

        if not email:
            return render(request, "complete_account.html", {
                "error": "Email address is required."
            })

        # Prevent another account from using the same email.
        if User.objects.filter(
            email__iexact=email
        ).exclude(
            id=request.user.id
        ).exists():

            return render(request, "complete_account.html", {
                "error": "This email is already registered with another account."
            })

        otp = str(random.randint(100000, 999999))

        request.session["account_email_otp"] = otp
        request.session["account_email_pending"] = email
        request.session["account_email_otp_time"] = time.time()

        request.session.modified = True

        send_mail(
            subject="Verify your email - E-Commerce",
            message=(
                f"Your email verification OTP is: {otp}\n\n"
                "This OTP is valid for 5 minutes.\n\n"
                "If you did not request this, please ignore this email."
            ),
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect("complete_account_verify")

    return render(request, "complete_account.html")

@login_required
def complete_account_verify(request):

    otp = request.session.get("account_email_otp")
    pending_email = request.session.get("account_email_pending")
    otp_time = request.session.get("account_email_otp_time")

    if not otp or not pending_email or not otp_time:
        return redirect("complete_account")

    # OTP expired
    if time.time() - float(otp_time) > OTP_EXPIRY_SECONDS:

        request.session.pop("account_email_otp", None)
        request.session.pop("account_email_pending", None)
        request.session.pop("account_email_otp_time", None)

        return render(request, "complete_account_verify.html", {
            "error": "OTP expired. Please request a new OTP."
        })

    if request.method == "POST":

        entered_otp = request.POST.get("otp", "").strip()

        if entered_otp != otp:
            return render(request, "complete_account_verify.html", {
                "error": "Invalid OTP. Please try again.",
                "email": pending_email
            })

        # Save email
        request.user.email = pending_email
        request.user.save(update_fields=["email"])

        # Clear OTP session
        request.session.pop("account_email_otp", None)
        request.session.pop("account_email_pending", None)
        request.session.pop("account_email_otp_time", None)

        request.session.modified = True

        return redirect("store")

    return render(request, "complete_account_verify.html", {
        "email": pending_email
    })