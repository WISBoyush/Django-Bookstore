from django.shortcuts import render, get_object_or_404

from django.views.generic.detail import DetailView

from django.contrib.contenttypes.models import ContentType


from django.db.models import Q

from cart.forms import CartAddProductForm
from .models import (Item,
                     Book,
                     Figure,
                     )


def main_page(request):
    search_result = request.GET.get('search', '')

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
