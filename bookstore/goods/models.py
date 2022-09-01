from django.contrib.contenttypes.models import ContentType
from django.db import models
from datetime import date

from django.utils.translation import gettext_lazy as _
from users.models import User
from profiles.models import Profile


class Tag(models.Model):
    tag_title = models.CharField(
        max_length=50
    )

    tag_description = models.CharField(
        max_length=100
    )

    discount = models.IntegerField(
        default=0
    )

    def __str__(self):
        return str(self.tag_title)


class Item(models.Model):
    quantity = models.IntegerField(
        default=0
    )

    title = models.CharField(
        max_length=50
    )

    description = models.TextField(
        max_length=1000
    )

    price = models.IntegerField(
        default=200
    )

    image = models.ImageField(
        null=True,
        upload_to=''
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='tags'
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.title)

    @property
    def price_discounted(self):
        items_discount = sum([item.get('discount') for item in self.tags.values('discount')])

        return self.price - (items_discount * 0.01) * self.price


class Service(models.Model):
    class State(models.TextChoices):
        CART = 'CART', _('In cart')
        AWAITING_ARRIVAL = 'AWAITING_ARRIVAL', _('Awaiting_arrival')
        AWAITING_PAYMENT = 'AWAITING_PAYMENT', _('Awaiting payment')
        PAID = 'PAID', _('Paid')
        AWAITING_DELIVERY = 'AWAITING_DELIVERY', _('Awaiting delivery')
        SENT = 'SENT', _('Sent')
        FINISHED = 'FINISHED', _('Finished')

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        blank=True,
        default=1
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        blank=True,
        default=1
    )

    state = models.CharField(
        max_length=50,
        choices=State.choices,
        default='CART'
    )

    orders_id = models.CharField(
        "ID of order",
        max_length=250,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


class Book(Item):
    author = models.CharField(
        max_length=100
    )

    date_of_release = models.DateField(
        "Date of release",
        auto_now=False,
        auto_now_add=False,
        default=date.today
    )

    type = 1


class Figure(Item):
    manufacturer = models.CharField(
        max_length=50
    )

    type = 2
