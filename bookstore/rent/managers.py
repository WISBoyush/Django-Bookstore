from django.db import models, transaction
from django.db.models import Count


class RentManager(models.Manager):
    def get_counted_data(self, **kwargs):
        return self.filter(**kwargs).values(
            'user_id',
            'item_id',
            'state',
            'rented_from',
            'rented_to',
            'city',
            'address',
            'orders_id',
            'item__title',
        ).annotate(
            amount=Count('item_id')
        )

    @transaction.atomic
    def add_entry_in_db(self, user_pk, item_id):
        self.create(
            state='CART',
            user_id=user_pk,
            item_id=item_id,
        )

    @transaction.atomic
    def delete_entry_in_db(self, item_id, user_pk):
        obj = self.filter(
            item_id=item_id,
            user_id=user_pk
        )

        obj.delete()
