from django.shortcuts import render
from django.views.generic.list import ListView
from .models import Product, Category


class ProductsListView(ListView):

    model = Product
    template_name = 'shop/listproducts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

def product_detail(request, id):
    return render(request, 'shop/productdetail.html')