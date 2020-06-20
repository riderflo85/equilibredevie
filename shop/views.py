from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from cart.forms import CartAddProductForm
from .forms import SearchProductForm, FilterProductForm
from .models import Product, Category
from .utils import filter_products_by_user_choice, filter_products_by_categories


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

        if 'filter_categ' in request.GET.keys():
            print("test in filter categ")
            all_products = filter_products_by_categories(
                request.GET['filter_categ']
            )
            context['category'] = request.GET['filter_categ']

        else:
            all_products = Product.objects.all()

        if 'filter_choice' in request.GET.keys():
            print('test in filter choice')
            data = {'filter_choice': request.GET['filter_choice']}
            filter_form = FilterProductForm(data)
            all_products = filter_products_by_user_choice(
                filter_form, all_products)
            context['filter'] = data

        else:
            filter_form = FilterProductForm()

        if all_products != "error":
            paginator = Paginator(all_products, 1)

            try:
                page_number = request.GET['page']
            except:
                page_number = 1

            page_obj = paginator.get_page(page_number)

            context['object_list'] = all_products
            context['page_obj'] = page_obj
            context['number_page'] = range(paginator.num_pages)
        else:
            context['error'] = "Le filtre de produit n'est pas valide."
    
    context['filter_form'] = filter_form
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
