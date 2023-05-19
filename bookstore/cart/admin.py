# from django.contrib import admin
# from django.contrib.admin import TabularInline, ModelAdmin
#
# from .models import Purchase
#
#
# class OrdersInline(TabularInline):
#     model = Purchase
#     fk_name = "fk_self"
#     extra = 0
#
#
# @admin.register(Purchase)
# class PurchaseAdmin(ModelAdmin):
#     inlines = [
#         OrdersInline
#     ]
