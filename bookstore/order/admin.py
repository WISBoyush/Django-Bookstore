from django.contrib import admin

from cart.models import Purchase
from rent.models import Rent


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "item_id",
        "state",
        "orders_time",
        "orders_id"
    )

    ordering = (
        "user_id",
        "orders_id"
    )

    list_filter = (
        "state",
        "user_id"
    )


@admin.register(Rent)
class RentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_id",
        "item_id",
        "state",
        "orders_id",
        "rented_from",
        "rented_to"
    )

    ordering = (
        "user_id",
        "orders_id"
    )

    list_filter = (
        "state",
        "user_id"
    )
