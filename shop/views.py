from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from cart.forms import CartAddProductForm
from .forms import SearchProductForm 
from .models import Product, Category


def list_all_products(request):
    context = {}

    if request.method == 'POST':
        search_form = SearchProductForm(request.POST)
        if search_form.is_valid():
            key_word = search_form.cleaned_data['search_product']

            try:
                search_products = Product.objects.filter(
                    name__icontains=key_word
                )
                context['matched'] = True
                context['object_list'] = search_products

            except:
                context['error'] = 'Aucun produit trouvés. :('

        else:
            context['error'] = 'Saisie de recherche non valide.'

    else:
        search_form = SearchProductForm()
        all_products = Product.objects.all()
        context['object_list'] = all_products
        
        paginator = Paginator(all_products, 1)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context['page_obj'] = page_obj
        context['number_page'] = range(paginator.num_pages)
    
    context['search_form'] = search_form
    context['categories'] = Category.objects.all()
    context['cart_product_form'] = CartAddProductForm()

    return render(request, 'shop/listproducts.html', context)

def product_detail(request, id_item):
    product = Product.objects.get(pk=id_item)
    related_product = Product.objects.filter(
        category=product.category).exclude(pk=product.pk)
    
    if len(related_product) > 4:
        related_product = related_product[:4]

    context = {
        "item": product,
        "related_item": related_product,
        "cart_product_form": CartAddProductForm()
    }
    return render(request, 'shop/productdetail.html', context)
