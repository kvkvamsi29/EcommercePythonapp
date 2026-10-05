from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


class Signup(View):

    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        # ============================
        # REQUIRED FIELDS
        # ============================
        if not username or not email or not password or not confirm_password:
            return render(request, "signup.html", {
                "error": "Username, email and password are required.",
                "username": username,
                "email": email,
            })

        # ============================
        # USERNAME CHECK
        # ============================
        if User.objects.filter(username=username).exists():
            return render(request, "signup.html", {
                "error": "Username already exists.",
                "username": username,
                "email": email,
            })

        # ============================
        # EMAIL CHECK
        # ============================
        if User.objects.filter(email__iexact=email).exists():
            return render(request, "signup.html", {
                "error": "This email is already registered.",
                "username": username,
                "email": email,
            })

        # ============================
        # PASSWORD MATCH
        # ============================
        if password != confirm_password:
            return render(request, "signup.html", {
                "error": "Passwords do not match.",
                "username": username,
                "email": email,
            })

        # ============================
        # DJANGO PASSWORD VALIDATION
        # ============================
        try:
            validate_password(password)
        except ValidationError as e:
            return render(request, "signup.html", {
                "error": " ".join(e.messages),
                "username": username,
                "email": email,
            })

        # ============================
        # CREATE USER
        # ============================
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Account created successfully. Please login."
        )

        return redirect("login")