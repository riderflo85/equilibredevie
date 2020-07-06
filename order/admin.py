from django.contrib import admin, messages
from django.utils.translation import ngettext
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
        'status',
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
    actions = ['update_order_status_send', 'update_order_status_prepare']

    def update_order_status_send(self, request, queryset):
        updated = queryset.update(status='send')
        self.message_user(request, ngettext(
            '%d Le statu de la commande a été changée avec succès.',
            '%d Le statu des commandes ont été changées avec succès.',
            updated,
        ) % updated, messages.SUCCESS)
    
    update_order_status_send.short_description = "Changer le statu en 'Expédié'."

    def update_order_status_prepare(self, request, queryset):
        updated = queryset.update(status='prepare')
        self.message_user(request, ngettext(
            '%d Le statu de la commande a été changée avec succès.',
            '%d Le statu des commandes ont été changées avec succès.',
            updated,
        ) % updated, messages.SUCCESS)

    update_order_status_prepare.short_description = "Changer le statu en \
        'En cours de préparation'."

@admin.register(OrderProductQuantity)
class OrderProductQuantityAdmin(admin.ModelAdmin):
    list_display = ['id_product', 'id_order', 'quantity', 'price']
    list_filter = ['id_product', 'id_order', 'quantity', 'price']
