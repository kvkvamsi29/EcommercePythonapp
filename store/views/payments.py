import random
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt



from django.http import JsonResponse
import random


from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def payment_page(request):
    return render(request, "payment.html")


@login_required
def place_order_cod(request):
    if request.method == "POST":
        # 🔒 DO NOT TOUCH your existing order logic
        # Just call your existing order creation method here
        # Example:
        # create_order(request.user)

        return redirect("order_success")

    return redirect("payment")


@login_required
def order_success(request):
    return render(request, "order_success.html")
