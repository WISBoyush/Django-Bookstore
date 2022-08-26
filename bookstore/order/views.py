from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import ListView, FormView
from django.db.models import Count

from cart.models import Purchase
from order.forms import PaymentForm
from profiles.models import Profile
from rent.models import Rent


class OrderHistoryView(ListView):
    model = Purchase
    context_object_name = 'order_history'
    template_name = 'order/history.html'

    def get_queryset(self):
        user_id = self.request.user.id

        purchase_order = Purchase.objects.get_counted_data(user_id=user_id)

        orders_ids = purchase_order.values('orders_id', 'total_orders_price', 'state').annotate(
            orders_positions=Count('orders_id'))

        history_list = []

        for order in orders_ids:
            history_list.append({'purchase_order_list': purchase_order.filter(orders_id=order['orders_id']),
                                 'orders_id': order['orders_id'],
                                 'total': order['total_orders_price'],
                                 'state': order['state']
                                 })

        return history_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class OrderRentHistoryView(ListView):
    model = Rent
    context_object_name = 'order_history'
    template_name = 'order/rent_history.html'

    def get_queryset(self):
        user_id = self.request.user.id

        rent_order = Rent.objects.get_counted_data(user_id=user_id)

        orders_ids = rent_order.values('orders_id', 'rented_from', 'rented_to', 'state').annotate(
            orders_positions=Count('orders_id'))

        history_list = []

        for order in orders_ids:
            history_list.append({'rent_order_list': rent_order.filter(orders_id=order['orders_id']),
                                 'orders_id': order['orders_id'],
                                 'state': order['state'],
                                 'rented_from': order['rented_from'],
                                 'rented_to': order['rented_to'],
                                 })

        return history_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        return context


class OrderPaymentView(FormView):
    context_object_name = 'order_payment'
    template_name = 'order/payment.html'
    form_class = PaymentForm

    def get_queryset(self):

        id_order = self.kwargs.get('order_id')

        return Purchase.objects.get_counted_data(orders_id=id_order)

    def get_context_data(self, **kwargs):

        context = super().get_context_data()

        order_inf = Purchase.objects.filter(orders_id=self.kwargs.get('order_id')).first()

        context['products'] = self.get_queryset()
        context['total'] = order_inf.total_orders_price
        context['order_id'] = order_inf.orders_id
        context['state'] = order_inf.state

        return context

    def post(self, request, *args, **kwargs):

        id_user = self.request.user.pk
        id_order = self.kwargs.get('order_id')

        cost = Purchase.objects.filter(orders_id=id_order).first().total_orders_price

        user = Profile.objects.filter(user_id=id_user).first()

        if cost > user.balance:

            messages.success(request, 'На вашем балансе недостаточно средств')

        else:

            user.balance -= cost
            user.save()

            messages.success(request, 'Заказ успешно оформлен, ожидайте более подробной информации')

            Purchase.objects.filter(orders_id=id_order).update(state='PAID')

        return redirect('payment', id_order)


class OrderRentStatusView(ListView):
    model = Rent
    template_name = 'order/rent_status.html'
    context_object_name = 'rent_status'

    def get_queryset(self):
        id_order = self.kwargs.get('order_id')

        return Rent.objects.get_counted_data(orders_id=id_order)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        order_inf = Rent.objects.filter(orders_id=self.kwargs.get('order_id')).first()
        context['products'] = self.get_queryset()
        context['order_id'] = order_inf.orders_id
        context['state'] = order_inf.state
        context['rented_from'] = order_inf.rented_from
        context['rented_to'] = order_inf.rented_to

        return context
