from django.db import models

from cart.managers import PurchaseManager
from goods.models import Service


class Purchase(Service):
    objects = PurchaseManager()

    warranty_days = models.IntegerField(
        "Dates of warranty",
        default=30
    )

    orders_time = models.DateTimeField(
        "Orders date time field",
        null=True,
        blank=True
    )

    city = models.CharField(
        'Delivery city',
        max_length=100,
        default='12345'
    )

    address = models.CharField(
        'Delivery address',
        max_length=250,
        default='12345'
    )

    total_orders_price = models.IntegerField(
        "Total price of order",
        null=True,
        blank=True
    )
