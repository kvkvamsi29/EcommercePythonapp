import random
import time

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


OTP_EXPIRY_SECONDS = 300  # 5 minutes


def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()

        if not email:
            return render(request, "forgot_password.html", {
                "error": "Email address is required."
            })

        try:
            user = User.objects.get(email__iexact=email)

        except User.DoesNotExist:
            return render(request, "forgot_password.html", {
                "error": "No account is registered with this email."
            })

        except User.MultipleObjectsReturned:
            return render(request, "forgot_password.html", {
                "error": "This email is associated with multiple accounts. Please contact support."
            })

        # ============================================================
        # PREVENT DUPLICATE OTP GENERATION
        # ============================================================
        existing_otp = request.session.get("password_reset_otp")
        existing_otp_time = request.session.get("password_reset_otp_time")
        existing_email = request.session.get("password_reset_email")

        if (
            existing_otp
            and existing_otp_time
            and existing_email == email
            and time.time() - float(existing_otp_time) <= OTP_EXPIRY_SECONDS
        ):
            return redirect("forgot_password_verify")

        # ============================================================
        # GENERATE ONE NEW OTP
        # ============================================================
        otp = str(random.randint(100000, 999999))

        request.session["password_reset_user_id"] = user.id
        request.session["password_reset_otp"] = otp
        request.session["password_reset_email"] = email
        request.session["password_reset_otp_time"] = time.time()

        # Make sure an old verification state cannot be reused.
        request.session.pop("password_reset_verified", None)

        request.session.modified = True

        # ============================================================
        # SEND OTP ONLY TO THE LOGGED-IN / REQUESTED EMAIL
        # ============================================================
        send_mail(
            subject="Password Reset OTP - E-Commerce",
            message=(
                f"Your password reset OTP is: {otp}\n\n"
                "This OTP is valid for 5 minutes.\n\n"
                "If you did not request a password reset, please ignore this email."
            ),
            from_email=None,
            recipient_list=[email],
            fail_silently=False,
        )

        return redirect("forgot_password_verify")

    return render(request, "forgot_password.html")


def forgot_password_verify(request):

    otp = request.session.get("password_reset_otp")
    user_id = request.session.get("password_reset_user_id")
    email = request.session.get("password_reset_email")
    otp_time = request.session.get("password_reset_otp_time")

    if not otp or not user_id or not email or not otp_time:
        return redirect("forgot_password")

    # ============================================================
    # OTP EXPIRY
    # ============================================================
    if time.time() - float(otp_time) > OTP_EXPIRY_SECONDS:

        request.session.pop("password_reset_otp", None)
        request.session.pop("password_reset_user_id", None)
        request.session.pop("password_reset_email", None)
        request.session.pop("password_reset_otp_time", None)
        request.session.pop("password_reset_verified", None)

        request.session.modified = True

        return render(request, "forgot_password_verify.html", {
            "error": "OTP expired. Please request a new OTP."
        })

    if request.method == "POST":

        entered_otp = request.POST.get("otp", "").strip()

        if entered_otp != otp:
            return render(request, "forgot_password_verify.html", {
                "error": "Invalid OTP. Please try again.",
                "email": email
            })

        # ============================================================
        # OTP VERIFIED
        # ============================================================

        request.session["password_reset_verified"] = True

        # IMPORTANT:
        # Destroy the OTP immediately after successful verification.
        # This prevents the same OTP from being reused.
        request.session.pop("password_reset_otp", None)
        request.session.pop("password_reset_otp_time", None)

        request.session.modified = True

        return redirect("reset_password_new")

    return render(request, "forgot_password_verify.html", {
        "email": email
    })


def reset_password_new(request):

    verified = request.session.get("password_reset_verified")
    user_id = request.session.get("password_reset_user_id")

    if not verified or not user_id:
        return redirect("forgot_password")

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return redirect("forgot_password")

    if request.method == "POST":

        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not password or not confirm_password:
            return render(request, "reset_password_new.html", {
                "error": "Both password fields are required."
            })

        if password != confirm_password:
            return render(request, "reset_password_new.html", {
                "error": "Passwords do not match."
            })

        try:
            validate_password(password, user)
        except ValidationError as e:
            return render(request, "reset_password_new.html", {
                "error": " ".join(e.messages)
            })

        user.set_password(password)
        user.save()

        # ============================================================
        # CLEAR PASSWORD RESET SESSION
        # ============================================================

        request.session.pop("password_reset_otp", None)
        request.session.pop("password_reset_user_id", None)
        request.session.pop("password_reset_email", None)
        request.session.pop("password_reset_otp_time", None)
        request.session.pop("password_reset_verified", None)

        request.session.modified = True

        messages.success(
            request,
            "Password reset successful. Please login with your new password."
        )

        return redirect("login")

    return render(request, "reset_password_new.html")