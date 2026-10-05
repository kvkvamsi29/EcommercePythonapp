from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from store.models.order import Order
from store.models.customer import Customer


@login_required
def orders(request):

    customer_email = (
        request.user.email
        or ""
    ).strip().lower()

    if not customer_email:

        return render(
            request,
            "orders.html",
            {
                "grouped_orders": []
            }
        )

    customer = (
        Customer.objects
        .filter(
            email__iexact=customer_email
        )
        .order_by("-id")
        .first()
    )

    if not customer:

        return render(
            request,
            "orders.html",
            {
                "grouped_orders": []
            }
        )

    raw_orders = (
        Order.objects
        .filter(customer=customer)
        .select_related("product")
        .order_by("-date", "-id")
    )

    grouped = defaultdict(list)

    for order in raw_orders:

        grouped[
            order.order_id
        ].append(order)

    STATUS_LABELS = {
        0: "Pending",
        1: "Shipped",
        2: "Delivered",
        3: "Cancelled",
    }

    grouped_orders = []

    for order_id, items in grouped.items():

        total = sum(
            (item.price or 0)
            for item in items
        )

        grouped_orders.append({
            "order_id": order_id,
            "date": items[0].date,
            "status": items[0].status,
            "address": items[0].address,
            "phone": items[0].phone,
            "items": items,
            "total": total,
            "group_status": STATUS_LABELS.get(
                items[0].status,
                "Pending"
            ),
        })

    grouped_orders.sort(
        key=lambda item: item["date"],
        reverse=True
    )

    return render(
        request,
        "orders.html",
        {
            "grouped_orders": grouped_orders
        }
    )


@login_required
def order_invoice(request, order_id):

    customer_email = (
        request.user.email
        or ""
    ).strip().lower()

    customer = (
        Customer.objects
        .filter(
            email__iexact=customer_email
        )
        .order_by("-id")
        .first()
    )

    if not customer:

        return HttpResponse(
            "Customer not found",
            status=404
        )

    orders = (
        Order.objects
        .filter(
            order_id=order_id,
            customer=customer
        )
        .select_related("product")
    )

    if not orders.exists():

        return HttpResponse(
            "Order not found",
            status=404
        )

    total = sum(
        order.price or 0
        for order in orders
    )

    response = HttpResponse(
        content_type="text/plain"
    )

    response[
        "Content-Disposition"
    ] = (
        f'attachment; '
        f'filename="invoice_{order_id}.txt"'
    )

    response.write(
        f"Invoice for Order ID: "
        f"{order_id}\n"
    )

    response.write(
        "-" * 40 + "\n"
    )

    for item in orders:

        response.write(
            f"{item.product.name} × "
            f"{item.quantity} = "
            f"₹{item.price}\n"
        )

    response.write(
        "-" * 40 + "\n"
    )

    response.write(
        f"TOTAL = ₹{total}\n"
    )

    return response