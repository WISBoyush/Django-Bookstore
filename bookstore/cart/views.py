import datetime
from uuid import uuid4

from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, get_object_or_404
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

        item = get_object_or_404(Item, id=item_id)

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

    # def total_price_discounted(self):
    #     products = Purchase.objects.total_items_price(self.user_pk)
    #     for product in products:
    #         product_discounted_price = Item.objects.filter(
    #             id=product['item_id']).first().price_discounted
    #         product['price_discounted'] = product['amount'] * product_discounted_price
    #         product['new_price'] = product_discounted_price
    #     #     product_list.append({
    #     #         'price_discounted': product['amount'] *
    #     #                           Item.objects.filter(id=product['item_id']).first().price_discount,
    #     #         'item_id': product['item_id'],
    #     #         'amount': product['amount']
    #     #     })
    #     # print(product_list)
    #     print(products)
    #     return products

    # return Item.objects.price_with_discount().filter(purchase__user_id=self.user_pk).annotate(
    #     amount=('id')).annotate(
    #     total_price_for_unit=F('discounted_price_for_unit') * F('amount')
    # )

    #     amounts = Item.objects.filter(purchase__user_id=self.user_pk).annotate(amount=Count('id')).values('id',
    #                                                                                                       'amount')
    #     obj = []
    #     for product in amounts:
    #         obj.append(Item.objects.price_with_discount().filter(purchase__user_id=self.user_pk,
    #                                                              id=product['id']).annotate(
    #             total_price_for_unit=F('discounted_price_for_unit') * product['amount'],
    #             amount=Value(product['amount'], output_field=models.IntegerField())))
    #
    #     return reduce(lambda i, j: i | j, obj)
    #
    # return Item.objects.all()

    # def get_total_price_of_buy(self):
    #     return sum([field['price_discounted'] for field in self.queryset])
    #
    # def get_persons_discounted_price(self):
    #     return self.context['total'] - self.get_personal_discount() * self.context['total']
    #
    # def get_personal_discount(self):
    #     return Profile.objects.filter(user_id=self.user_pk).first().person_disc * 0.01

    # def get_queryset(self):
    #     self.user_pk = self.request.user.pk
    #     self.queryset = self.total_price_discounted()
    #     # session_cotext = [[[item_key, item_value] for item_key, item_value in item.items()] for item in
    #     #                   self.queryset.values()]
    #     # self.request.session['shopping_cart'] = session_cotext
    #     # P.s. Send context in session
    #     return self.queryset
    #
    # def get_context_data(self, *, object_list=None, **kwargs):
    #     self.context = super().get_context_data()
    #     self.context['total'] = self.get_total_price_of_buy()
    #     self.context['persons_discounted_price'] = self.get_persons_discounted_price()
    #     # session_cotext = self.context.loads()
    #     # self.request.session['shopping_cart'] = session_cotext
    #     return self.context

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

        self.queryset = Purchase.objects.get_total_products_information(user_pk=user_pk)

        return self.queryset

    def get_context_data(self, **kwargs):

        self.context = super().get_context_data()

        return self.context

    @transaction.atomic
    def order_process(self, request, forms_data, total_order_price):

        Purchase.objects.filter(user_id=self.request.user.pk, state='CART').prefetch_related(
            'item__purchase_set').update(
            orders_time=datetime.datetime.now(),
            city=forms_data['city'],
            address=forms_data['address'],
            orders_id=uuid4(),
            total_orders_price=total_order_price)

        orders_product = Purchase.objects.filter(user_id=self.request.user.pk, state='CART').select_related(
            'item')

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
