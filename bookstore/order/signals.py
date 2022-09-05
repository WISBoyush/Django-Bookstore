from django.db import transaction
from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from cart.models import Purchase
from goods.models import Item
from order.tasks import order_created


@transaction.atomic
@receiver(post_save, sender=Item)
def update(sender, instance, update_fields, **kwargs):
    order_awaiting_refill = Purchase.objects.filter(
        state='AWAITING_ARRIVAL'
    ).order_by(
        'orders_time'
    ).first()

    if order_awaiting_refill is not None:

        items_amount = Purchase.objects.filter(orders_id=order_awaiting_refill.orders_id).values(
            'item_id'
        ).annotate(
            amount=(Count('item_id'))
        ).order_by('item_id')

        all_products = Item.objects.filter(id__in=[item['item_id'] for item in items_amount])

        if all(
                [all_products.get(
                    id=item['item_id']
                ).quantity
                 >= item['amount']
                 for item in items_amount]
        ):
            Purchase.objects.filter(orders_id=order_awaiting_refill.orders_id
                                    ).update(
                state='AWAITING_PAYMENT'
            )

            order_created.delay(
                order_id=order_awaiting_refill.orders_id
            )
