from django.urls import path
from cart.views import OrderView
from .views import (
    OrderHistoryView,
    OrderPaymentView,
    OrderRentHistoryView,
    OrderRentStatusView
)


urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('purchase_history/', OrderHistoryView.as_view(), name='purchase_history'),
    path('rent_history/', OrderRentHistoryView.as_view(), name='rent_history'),
    path('payment/<str:order_id>', OrderPaymentView.as_view(), name='payment'),
    path('rent_status/<str:order_id>', OrderRentStatusView.as_view(), name='rent_status')
]
