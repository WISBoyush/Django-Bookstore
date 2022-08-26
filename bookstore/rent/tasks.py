from celery import shared_task
from django.core.mail import send_mail

from bookstore.settings import EMAIL_HOST_USER
from .models import Rent


@shared_task
def rent_order_created(order_id):
    order = Rent.objects.filter(orders_id=order_id).first()

    return send_mail('Order nr. {}'.format(order_id),
                     'Dear {},\n\n'
                     'Your order has been successfully processed'
                     'Your order\'s link is http://127.0.0.1:8000/cart/order/rent_status/{} .'
                     .format(order.user.email,
                             order_id),
                     EMAIL_HOST_USER,
                     [order.user.email])
