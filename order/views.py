from datetime import datetime
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, OrderProductQuantity
from .check_stripe_client import check_stripe_client
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def create_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        data = request.POST
        datetime_ref = datetime.now()
        datetime_ref = datetime_ref.strftime("%d%m%Y%H%M%S%f")
        user = request.user
        user_customer = check_stripe_client(stripe, user, data['dep'])

        order = Order()
        order.reference = datetime_ref
        order.total_price = cart.get_total_price()
        order.note = data['note']


        if data['another_adress'] == 'true':
            order.last_name = data['anLN']
            order.first_name = data['anFN']
            order.adress = data['anAd']
            order.postal_code = int(data['anCP'])
            order.city = data['anCi']
            order.dep = data['anDe']
            order.phone_number = int(data['anPN'])
            order.email = data['anEm']

        elif data['another_adress'] == 'false':
            order.last_name = data['last_name']
            order.first_name = data['first_name']
            order.adress = data['adress']
            order.postal_code = int(data['postal_code'])
            order.city = data['city']
            order.dep = data['dep']
            order.phone_number = int(data['phone_number'])
            order.email = data['email']
        order.save()

        for item in cart:
            product_order = OrderProductQuantity()
            product_order.id_product = item['product']
            product_order.id_order = order
            product_order.quantity = item['quantity']
            product_order.price = item['price']
            product_order.save()

        session = stripe.checkout.Session.create(
            customer=user_customer,
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'unit_amount_decimal': cart.get_total_price()*100,
                    'currency': 'eur',
                    'product': settings.STRIPE_PRODUCT,
                    },
                'quantity': 1,
            }],
            mode='payment',
            success_url=f"{settings.SUCCES_URL_PAYMENT}&ref={order.reference}",
            cancel_url=f"{settings.ERROR_URL_PAYMENT}?ref={order.reference}"
        )
        order.stripe_id = session['payment_intent']
        order.save()
        user.order.add(order)
        cart.clear()
        request.session.modified = True

        return JsonResponse({
            'success': True,
            'ref': datetime_ref,
            'stripe_session': session['id'],
            "key": settings.STRIPE_PUBLISHABLE_KEY
        })

    else:

        return render(request, 'order/createorder.html', {"key": settings.STRIPE_PUBLISHABLE_KEY})

def success_order(request):
    ref_order = request.GET['ref']
    order = get_object_or_404(Order, reference=ref_order)
    context = {
        'order': order
    }

    response = stripe.PaymentIntent.retrieve(order.stripe_id)

    if response['status'] == 'succeeded':
        order.paid = True
        order.save()
    
    return render(request, 'order/ordersuccess.html', context)

def fail_order(request):
    ref_order = request.GET['ref']

    context = {
        'order': get_object_or_404(Order, reference=ref_order)
    }
    return render(request, 'order/orderfail.html', context)

def test_view(request):
    print(request.GET)
    return render(request, 'order/createorder.html', {"key": settings.STRIPE_PUBLISHABLE_KEY})