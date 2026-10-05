from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from store.models.product import Products
from store.models.customer import Customer

class Order(models.Model):

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Products, on_delete=models.CASCADE, null=True, blank=True)

    quantity = models.IntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)

    status = models.IntegerField(default=0)

    # ✅ SAFE date field (no auto_now_add migration break)
    date = models.DateTimeField(default=timezone.now, null=True, blank=True)

    order_id = models.CharField(max_length=50, null=True, blank=True)
    
    class Meta:
      ordering = ["-date", "-id"]
    
    def __str__(self):
        return f"Order #{self.id}"
