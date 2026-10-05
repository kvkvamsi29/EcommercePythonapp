from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def order_success(request):
    order_id = request.session.pop("last_order_id", None)
   
    return render(request, "store/order_success.html", {
        "order_id": order_id
    })
