from celery import shared_task
from django.core.mail import send_mail

from bookstore.settings import EMAIL_HOST_USER
from cart.models import Purchase


@shared_task
def order_created(order_id):
    order = Purchase.objects.filter(orders_id=order_id).first()
    if order:
        return send_mail('Order nr. {}'.format(order_id),
                         'Dear {},\n\n'
                         'Your order has been successfully processed and is awaiting payment'
                         'Your order\'s link is http://127.0.0.1:8000/cart/order/payment/{} .'
                         .format(order.user.email,
                                 order_id),
                         EMAIL_HOST_USER,
                         [order.user.email])
