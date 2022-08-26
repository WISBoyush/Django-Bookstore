from django.db import transaction
from django.db.models import Count, F
from django.db.models.signals import post_save
from django.dispatch import receiver

from goods.models import Item
from cart.models import Purchase
from order.tasks import order_created


@transaction.atomic
@receiver(post_save, sender=Item)
def update(sender, instance, update_fields, **kwargs):

    awaiting_user = Purchase.objects.filter(
        state='AWAITING_ARRIVAL'
    ).order_by(
        'orders_time'
    ).values(
        'orders_id',
        'item_id'
    )

    if awaiting_user.exists():

        awaiting_user = awaiting_user.first()

        items_amount = Purchase.objects.filter(orders_id=awaiting_user['orders_id']).values(
            'item_id'
        ).annotate(
            amount=(Count('item_id'))
        )

        if all(
                [Item.objects.filter(
                    id=item['item_id']
                ).values('quantity').first()['quantity']
                 >= item['amount']
                 for item in items_amount]
        ):

            Purchase.objects.filter(orders_id=awaiting_user['orders_id']
                                    ).update(
                state='AWAITING_PAYMENT'
            )

            for item in items_amount:

                Item.objects.filter(id=item['item_id']).update(
                    quantity=F('quantity') - item['amount']
                )

            order_created.delay(
                order_id=awaiting_user['orders_id']
            )
