from django.db import models


class DummyPayment(models.Model):
    """
    Disabled placeholder model.
    DO NOT use ORM operations on this model.
    Exists only to keep old imports safe.
    """

    class Meta:
        managed = False
        db_table = "dummy_disabled"
