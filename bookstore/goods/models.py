from datetime import date
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from profiles.models import Profile
from users.models import User


class Tag(models.Model):
    tag_title = models.CharField(
        max_length=50,
        verbose_name=_("Tag's title")
    )

    tag_description = models.CharField(
        max_length=100,
        verbose_name=_("Tag's description")
    )

    discount = models.IntegerField(
        default=0,
        verbose_name=_('Discount')
    )

    def __str__(self):
        return str(self.tag_title)


class Item(models.Model):
    quantity = models.IntegerField(
        default=0,
        verbose_name=_('Quantity')
    )

    title = models.CharField(
        max_length=50,
        verbose_name=_('Title')
    )

    description = models.TextField(
        max_length=1000,
        verbose_name=_('Description')
    )

    price = models.IntegerField(
        default=200,
        verbose_name=_('Price')
    )

    image = models.ImageField(
        null=True,
        upload_to='',
        verbose_name=_('Image')
    )

    tags = models.ManyToManyField(
        Tag,
        verbose_name='tags'
    )

    content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        verbose_name=_('Content type')
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
        default=1,
        verbose_name=_('User')
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        blank=True,
        default=1,
        verbose_name=_('Item')
    )

    state = models.CharField(
        max_length=50,
        choices=State.choices,
        default='CART',
        verbose_name=_('State')
    )

    orders_id = models.CharField(
        max_length=250,
        null=True,
        blank=True,
        verbose_name=_("Order's id")
    )

    class Meta:
        abstract = True


class Book(Item):
    author = models.CharField(
        max_length=100,
        verbose_name=_('Author')
    )

    date_of_release = models.DateField(
        auto_now=False,
        auto_now_add=False,
        default=date.today,
        verbose_name=_('Date of release')
    )

    type = 1


class Figure(Item):
    manufacturer = models.CharField(
        max_length=50,
        verbose_name=_('Manufacturer')
    )

    type = 2
