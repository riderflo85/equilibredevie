from django.contrib import admin
from .models import Order, OrderProductQuantity


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = [
        'reference',
        'last_name',
        'first_name',
        'adress',
        'postal_code',
        'city',
        'dep',
        'phone_number',
        'email',
        'created',
        'updated',
        'paid',
        'receipt_send',
        'validate_order_send',
        'invoice_send',
        'stripe_id',
        'url_receipt',
        'total_price',
        'note'
    ]
    list_filter = [
        'reference',
        'last_name',
        'first_name',
        'dep',
        'created',
        'total_price'
    ]

@admin.register(OrderProductQuantity)
class OrderProductQuantityAdmin(admin.ModelAdmin):
    list_display = ['id_product', 'id_order', 'quantity', 'price']
    list_filter = ['id_product', 'id_order', 'quantity', 'price']
