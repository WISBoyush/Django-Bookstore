from django.db import models
from django.db.models import Count

from goods.models import Item
from profiles.models import Profile


class PurchaseManager(models.Manager):

    def get_items_amount(self):
        # Amount of items in shopping cart.
        products = self.filter(user_id=self.user_pk, state='CART').values(
            'item_id',
            'user_id',
            'state',
            'address',
            'city',
            'warranty_days',
            'orders_time',
            'item__price',
            'item__title',
        ).annotate(
            amount=Count('item_id'))
        return products

    def total_price_discounted(self):
        products = self.get_items_amount()

        for product in products:
            product_discounted_price = Item.objects.filter(
                id=product['item_id']).first().price_discounted

            product['price_discounted'] = product['amount'] * product_discounted_price
            product['new_price'] = product_discounted_price

        return products

    def get_total_price_of_buy(self):
        return sum([field['price_discounted'] for field in self.items_price])

    def get_persons_discounted_price(self):
        return self.total_products_inf['total'] - self.get_personal_discount() * self.total_products_inf['total']

    def get_personal_discount(self):
        return Profile.objects.filter(user_id=self.user_pk).first().person_disc * 0.01

    def get_total_products_information(self, user_pk):
        self.user_pk = user_pk
        self.items_price = self.total_price_discounted()
        self.total_products_inf = dict()
        self.total_products_inf['total'] = self.get_total_price_of_buy()
        self.total_products_inf['persons_discounted_price'] = self.get_persons_discounted_price()
        self.total_products_inf['products'] = self.items_price

        return self.total_products_inf

    def get_counted_data(self, **kwargs):
        return self.filter(**kwargs).values(
            'user_id',
            'item_id',
            'state',
            'orders_time',
            'city',
            'address',
            'orders_id',
            'item__title',
            'item__price',
            'total_orders_price'
        ).annotate(
            amount=Count('item_id')
        )
