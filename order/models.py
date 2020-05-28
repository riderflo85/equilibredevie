from django.db import models
from shop.models import Product


class Order(models.Model):
    reference = models.CharField(
        max_length=21, verbose_name='Référence de la commande'
    )
    last_name = models.CharField(max_length=150)
    first_name = models.CharField(max_length=30)
    adress = models.CharField(max_length=350)
    postal_code = models.IntegerField()
    city = models.CharField(max_length=250)
    dep = models.CharField(max_length=100)
    phone_number = models.IntegerField()
    email = models.EmailField()
    another_delivery_adress = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    receipt_send = models.BooleanField(default=False)
    validate_order_send = models.BooleanField(default=False)
    invoice_send = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=150, blank=True)
    url_receipt = models.CharField(max_length=300)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.TextField(blank=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return 'Order {}'.format(self.id)
    
    def get_total_price(self):
        return sum(item.get_price() for item in self.items.all())


class OrderProductQuantity(models.Model):
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, verbose_name='Quantité')
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return '{}'.format(self.id)

    def get_price(self):
        return self.price * self.quantity
