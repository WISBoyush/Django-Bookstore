from django.db import models
from datetime import date

from goods.models import Service
from .managers import RentManager


class Rent(Service):
    rented_from = models.DateField(
        "Rented from",
        auto_now=False,
        auto_now_add=False,
        default=date.today
    )

    rented_to = models.DateField(
        "Rented to",
        auto_now=False,
        auto_now_add=False,
        default=date.today
    )

    city = models.CharField(
        "City to delivery",
        max_length=100,
        null=False,
        blank=False,
        default='12345'
    )

    address = models.CharField(
        "Address to delivery",
        max_length=100,
        null=False,
        blank=False,
        default='12345'
    )

    objects = RentManager()
