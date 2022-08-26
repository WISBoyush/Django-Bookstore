import django.contrib.auth
from django.urls import path, include
from django.conf import settings
from . import views
from .views import CartPurchaseView

urlpatterns = [
    path('cart/detail', CartPurchaseView.as_view(), name='cart_detail'),
    path('cart/<int:item_id>/add/', views.AddPurchaseView.as_view(), name='cart_add'),
    path('cart/<int:item_pk>/remove/', views.DeleteItemPurchaseView.as_view(), name='cart_remove'),
    path('cart/order/', include('order.urls'))
]