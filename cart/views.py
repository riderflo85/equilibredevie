from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from shop.models import Product
from shop.utils import get_product_declination
from .cart import Cart
from .forms import CartAddProductForm


def index_cart(request):
    cart = Cart(request)

    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                                        initial={
                                            'quantity': item['quantity'],
                                            'update': True
                                            })

    return render(request, 'cart/cart.html', {'cart': cart})

def remove_product_in_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart')

def remove_product_in_mini_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return JsonResponse({'success': True})

@require_POST
def add_product_in_cart(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)

    if product.has_a_declination:
        declinations, declination_type = get_product_declination(product)
        form = CartAddProductForm(
            request.POST,
            declination=declinations,
            declination_type=declination_type
        )

    else:
        form = CartAddProductForm(request.POST)

    if form.is_valid():
        cd = form.cleaned_data

        if 'declination' in cd.keys() and cd['declination'] != '':
            product = Product.objects.get(pk=int(cd['declination']))

        cart.add(
            product=product,
            quantity=cd['quantity'],
            update_quantity=cd['update']
        )

    return redirect('shop:shop')

@require_POST
def update_cart(request):
    data = request.POST['data'].split('|')
    data.pop(-1)
    
    cart = Cart(request)

    if cart.update(data):
        return JsonResponse({'success': True})

    else:
        return JsonResponse({'success': False})
