from django.urls import path
from .views import (
    AddToRentView,
    RentCartView,
    MakeRentOrder,
    RemoveRentOrdersItem
)

urlpatterns = [
    path('rent_add/<int:item_id>', AddToRentView.as_view(), name="rent_add"),
    path('rent/detail', RentCartView.as_view(), name="rent_detail"),
    path('rent/make_order', MakeRentOrder.as_view(), name='rent_order'),
    path('rent_delete/<int:item_id>', RemoveRentOrdersItem.as_view(), name='rent_cart_remove')
]
