from django.shortcuts import render
from django.core.paginator import Paginator
from django.views.generic.list import ListView
from cart.forms import CartAddProductForm
from .forms import SearchProductForm, FilterProductForm
from .models import Product, Category, ProductDeclination
from .utils import filter_products_by_user_choice, \
filter_products_by_categories, get_product_declination


def list_all_products(request):
    context = {}
    all_products = None

    if request.method == 'POST':
        search_form = SearchProductForm(request.POST)
        if search_form.is_valid():
            key_word = search_form.cleaned_data['search_product']

            try:
                search_products = Product.objects.filter(
                    name__icontains=key_word
                ).exclude(is_a_declination=True)
                all_products = search_products
                context['matched'] = True
                context['object_list'] = search_products

            except:
                context['error'] = 'Aucun produit trouvés. :('

        else:
            context['error'] = 'Saisie de recherche non valide.'

    else:
        search_form = SearchProductForm()

        if 'filter_categ' in request.GET.keys():
            all_products = filter_products_by_categories(
                request.GET['filter_categ']
            )
            context['category'] = request.GET['filter_categ']

        else:
            all_products = Product.objects.all().exclude(is_a_declination=True)

        if 'filter_choice' in request.GET.keys():
            data = {'filter_choice': request.GET['filter_choice']}
            filter_form = FilterProductForm(data)
            all_products = filter_products_by_user_choice(
                filter_form, all_products)
            context['filter'] = data

        else:
            filter_form = FilterProductForm()

    if all_products != "error" and len(all_products) > 0:
        paginator = Paginator(all_products, 3)

        try:
            page_number = request.GET['page']
        except:
            page_number = 1

        page_obj = paginator.get_page(page_number)

        context['object_list'] = all_products
        context['page_obj'] = page_obj
        context['number_page'] = range(paginator.num_pages)
        try:
            context['filter_form'] = filter_form
        except UnboundLocalError:
            context['filter_form'] = FilterProductForm()
    else:
        context['error'] = "Le filtre de produit n'est pas valide."

    context['search_form'] = search_form
    context['categories'] = Category.objects.all()
    context['cart_product_form'] = CartAddProductForm()

    return render(request, 'shop/listproducts.html', context)

def product_detail(request, id_item):
    product = Product.objects.get(pk=id_item)
    related_product = Product.objects.filter(
        category=product.category
    ).exclude(pk=product.pk).exclude(is_a_declination=True)
    
    if len(related_product) >= 3:
        related_product = related_product[:3]
    
    print(related_product)

    context = {
        "item": product,
        "related_item": related_product,
    }

    if product.has_a_declination:
        declinations, declination_type = get_product_declination(product)
        context['cart_product_form'] = CartAddProductForm(
            declination=declinations,
            declination_type=declination_type
        )
        context['declinations'] = True

    else:
        context['cart_product_form'] = CartAddProductForm()
        context['declinations'] = False

    return render(request, 'shop/productdetail.html', context)
