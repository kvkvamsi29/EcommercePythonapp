from django.db import models


class Products(models.Model):
    is_latest = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    rating = models.FloatField(default=0)
    reviews = models.JSONField(default=list, blank=True)
    description = models.TextField(blank=True, default="")
    image = models.URLField(max_length=500)
    api_phone_id = models.CharField(
    max_length=255,
    blank=True,
    null=True,
    help_text="Mobile Phones API phone ID"
)

    specifications = models.JSONField(default=dict, blank=True)
    features = models.JSONField(default=list, blank=True)

    category = models.ForeignKey(
        "Category",          # ✅ STRING REFERENCE
        on_delete=models.CASCADE
    )

    product_type = models.CharField(
        max_length=20,
        choices=[
            ('mobile', 'Mobile'),
            ('tablet', 'Tablet'),
            ('laptop', 'Laptop')
        ],
        default='mobile'
    )

    def __str__(self):
        return self.name

    @property
    def features_list(self):
        return self.features or []

    @property
    def specs_dict(self):
        return self.specifications or {}
