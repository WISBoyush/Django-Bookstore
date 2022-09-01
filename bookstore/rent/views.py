import datetime
import logging
from uuid import uuid4

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.db.models import F
from django.shortcuts import redirect
from django.views.generic import (
    View,
    ListView,
    CreateView,
    DeleteView
)

from datetime import date

from goods.models import Item
from rent.models import Rent
from .forms import AddToRentForm, MakeRentOrderForm
from .tasks import rent_order_created

logger = logging.getLogger(__name__)


class AddToRentView(View):
    form_class = AddToRentForm

    @transaction.atomic
    def add_entry_in_db(self, user_pk, item_id):
        Rent.objects.create(
            state='CART',
            user_id=user_pk,
            item_id=item_id,
        )

    def post(self, request, *args, **kwargs):

        user_pk = request.user.pk

        if not user_pk:
            return redirect('login')

        item_id = self.kwargs.get('item_id')

        amount_in_stock = Item.objects.get(id=item_id).quantity

        rented_product_in_cart = Rent.objects.filter(user_id=user_pk, state='CART', item_id=item_id)

        if not amount_in_stock:

            messages.error(request, 'На данный момент товара нет на складе')

            return redirect('items_detail', item_id)

        if not rented_product_in_cart.exists():

            Rent.objects.add_entry_in_db(user_pk=user_pk, item_id=item_id)

            return redirect('main_page_url')

        else:

            messages.error(request, 'Данный товар уже находится в вашей корзине проката')
            return redirect('items_detail', item_id)


class RentCartView(ListView):
    template_name = 'cart/rent_detail.html'
    model = Rent
    context_object_name = 'rented_objects'

    def get_queryset(self):
        return Rent.objects.filter(user_id=self.request.user.pk, state='CART').values(
            'item__title',
            'item_id'
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['rented_to'] = date.today() + datetime.timedelta(days=14)
        return context


class MakeRentOrder(LoginRequiredMixin, CreateView, ListView):
    context_object_name = 'ordered_objects'
    form_class = MakeRentOrderForm
    template_name = 'order/rent_order.html'


    def get_queryset(self):
        return Rent.objects.filter(user_id=self.request.user.pk, state='CART').values(
            'item__title',
            'item_id'
        )

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['rented_to'] = date.today() + datetime.timedelta(days=14)
        return context

    @transaction.atomic
    def rent_order_process(self, ordered_products):
        objects_ids = [product.pk for product in ordered_products]

        Item.objects.filter(id__in=objects_ids).update(
            quantity=F('quantity') - 1
        )
        order_id = uuid4()
        ordered_products.update(
            rented_from=date.today(),
            rented_to=date.today() + datetime.timedelta(days=14),
            state='AWAITING_DELIVERY',
            orders_id=order_id
        )
        try:

            rent_order_created.delay(
                order_id=order_id
            )

        except Exception as e:

            logger.error(f'{e}')

    def post(self, request, *args, **kwargs):
        ordered_products = Rent.objects.filter(user_id=self.request.user.pk, state='CART')

        self.rent_order_process(ordered_products)

        return redirect('rent_history')


class RemoveRentOrdersItem(DeleteView):

    def delete(self, request, *args, **kwargs):

        user_pk = self.request.user.pk

        item_id = self.kwargs.get('item_id')

        Rent.objects.delete_entry_in_db(user_pk=user_pk, item_id=item_id)

        return redirect('rent_detail')

    def post(self, request, *args, **kwargs):
        return self.delete(self, request, *args, **kwargs)
