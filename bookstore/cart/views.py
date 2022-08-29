import datetime
from uuid import uuid4

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect
from django.db.models import F, Count
from goods.models import Item
from .models import Purchase
from .forms import CartAddProductForm, OrderForm
from django.views.generic import *


class AddPurchaseView(View):
    form_class = CartAddProductForm
    model = Purchase

    def post(self, request, *args, **kwargs):

        user_pk = request.user.pk

        if not user_pk:
            return redirect('login')

        item_id = self.kwargs.get('item_id')

        form = CartAddProductForm(request.POST)

        data_form = form.data

        for record in range(int(data_form['quantity'])):
            Purchase.objects.create(
                warranty_days=14,
                state='CART',
                user_id=user_pk,
                item_id=item_id,
            )

        return redirect('main_page_url')


class CartPurchaseView(ListView):
    context_object_name = 'cart'
    template_name = 'cart/detail.html'
    model = Purchase

    def get_queryset(self):
        user_pk = self.request.user.pk

        self.queryset = Purchase.objects.get_total_products_information(user_pk=user_pk)

        return self.queryset

    def get_context_data(self, **kwargs):
        self.context = super().get_context_data()

        return self.context


class DeleteItemPurchaseView(DeleteView):

    def delete(self, request, *args, **kwargs):
        user_pk = self.request.user.pk

        item_id = self.kwargs.get('item_pk')

        obj = Purchase.objects.filter(
            item_id=item_id,
            user_id=user_pk
        )

        obj.delete()

        return redirect('cart_detail')

    def post(self, request, *args, **kwargs):
        return self.delete(self, request, *args, **kwargs)


class OrderView(CreateView, ListView):
    form_class = OrderForm
    context_object_name = 'order'
    template_name = 'order/order.html'

    def get_queryset(self):

        user_pk = self.request.user.pk

        # TODO Просто вернуть куэрисет
        self.queryset = Purchase.objects.get_total_products_information(user_pk=user_pk)

        return self.queryset

    def get_context_data(self, **kwargs):

        self.context = super().get_context_data()

        return self.context

    @transaction.atomic
    def order_process(self, request, forms_data, total_order_price):

        Purchase.objects.filter(
            user_id=self.request.user.pk,
            state='CART'
        ).prefetch_related('item__purchase_set').update(
            orders_time=datetime.datetime.now(),
            city=forms_data['city'],
            address=forms_data['address'],
            orders_id=uuid4(),
            total_orders_price=total_order_price
        )

        orders_product = Purchase.objects.filter(
            user_id=self.request.user.pk,
            state='CART'
        ).select_related('item')

        #TODO Переименовать чтобы было понятно
        amount_of_orders_product = orders_product.values('item_id', 'state',
                                                         'item__quantity', 'item'
                                                         ).annotate(amount=Count('item_id'))

        if any(product['amount'] >= product['item__quantity'] for product in amount_of_orders_product):

            amount_of_orders_product.update(state='AWAITING_ARRIVAL')

            messages.success(request,
                             'The order was successfully created, but at the moment we do not have enough goods in '
                             'stock, the delivery will be slightly delayed'
                             )
        else:

            for product in amount_of_orders_product:
                Item.objects.filter(id=product['item_id']
                                    ).update(
                    quantity=F('quantity') - product['amount']
                )

            amount_of_orders_product.update(state='AWAITING_PAYMENT')

            messages.success(request, 'Order was successfully created')

    def post(self, request, *args, **kwargs):

        total_order_price = Purchase.objects.get_total_products_information(user_pk=self.request.user.pk)[
            'persons_discounted_price']

        forms_data = self.get_form().data

        self.order_process(request, forms_data, total_order_price)

        return redirect('cart_detail')
