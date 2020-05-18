from datetime import datetime
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from .models import Order, OrderProductQuantity


@login_required
def create_order(request):
    if request.method == 'POST':
        cart = Cart(request)
        data = request.POST
        datetime_ref = datetime.now()
        datetime_ref = datetime_ref.strftime("%d%m%Y%H%M%S%f")
        user = request.user

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
        
        order.paid = True
        order.save()
        user.order.add(order)
        cart.clear()
        request.session.modified = True

        return JsonResponse({'success': True, 'ref': datetime_ref})

    else:
        return render(request, 'order/createorder.html')

def success_order(request, ref_order):
    context = {
        'order': get_object_or_404(Order, reference=ref_order)
    }
    return render(request, 'order/ordersuccess.html', context)