from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView

from django.views.generic.detail import DetailView

from django.contrib.contenttypes.models import ContentType

from django.contrib.auth.views import (LoginView,
                                       LogoutView,
                                       PasswordResetView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetCompleteView
                                       )

from django.db.models import Q

from cart.forms import CartAddProductForm
from .models import (Item,
                     Tag,
                     Book,
                     Figure,
                     User,
                     Profile
                     )
# from .forms import UserRegistrationForm, UserLogin


def main_page(request):
    search_result = request.GET.get('search', '')
    items_types = [Book, Figure]

    if search_result:

        books_list = Book.objects.filter(Q(title__icontains=search_result.lower()) |
                                         Q(description__icontains=search_result.lower()))

        figures_list = Figure.objects.filter(Q(title__icontains=search_result.lower()) |

                                             Q(description__icontains=search_result.lower()))
    else:

        books_list = Book.objects.all()

        figures_list = Figure.objects.all()

    context = {'books_list': books_list,
               'figures_list': figures_list}

    return render(request, 'index.html', context)


class ItemDetailView(DetailView):
    context_object_name = 'detail_item'
    template_name = 'detail.html'

    def get_queryset(self):
        current_item = get_object_or_404(Item, pk=self.kwargs.get('pk'))

        item_type = ContentType.objects.filter(
            model=current_item.content_type.model
        ).first().model_class()

        return item_type.objects.filter(
            pk=self.kwargs.get('pk')
        )

    def get_context_data(self, **kwargs):

        context = super().get_context_data()

        context['cart_product_form'] = CartAddProductForm()

        return context

        # def item_detail(request, id):
    #     product = get_object_or_404(Item,
    #                                 id=id,
    #                                 available=True)
    #     cart_product_form = CartAddProductForm()
    #     return render(request, 'detail.html', {'product': product,
    #                                            'cart_product_form': cart_product_form})


# class RegisterFormView(CreateView):
#     template_name = 'registration/register.html'
#     form_class = UserRegistrationForm
#
#     def get_success_url(self):
#
#         return reverse_lazy('login')
#
#
# class UserLoginView(LoginView):
#     template_name = 'registration/login.html'
#     form_class = UserLogin
#
#     def get_success_url(self):
#
#         return reverse_lazy('main_page_url')
#
#
# class UserLogoutView(LogoutView):
#     template_name = 'registration/logout.html'


# class ProfileData(ListView):
#     template_name = 'profile.html'
#     context_object_name = 'element'
#
#     def get_queryset(self):
#
#         user = self.request.session['_auth_user_id']
#
#         current_item = Profile.objects.filter(user_id=user).first()
#
#         return current_item
#
#     def get_context_data(self, *, object_list=None, **kwargs):
#
#         context = super().get_context_data()
#
#         return context


# class UserPasswordResetView(PasswordResetView):
#     template_name = 'password/password-reset.html'
#
#
# class UserPasswordResetDoneView(PasswordResetDoneView):
#     template_name = 'password/password-reset-done.html'
#
#
# class UserPasswordResetConfirmView(PasswordResetConfirmView):
#     template_name = 'password/password-reset-confirm.html'
#
#     def get_success_url(self):
#         return reverse_lazy('password_reset_complete')
#
#
# class UserPasswordResetCompleteView(PasswordResetCompleteView):
#     template_name = 'password/password-reset-complete.html'
