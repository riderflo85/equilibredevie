from django.db import models
from shop.models import Product


class Order(models.Model):
    reference = models.CharField(
        max_length=50, verbose_name='Référence de la commande'
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    stripe_id = models.CharField(max_length=150, blank=True)
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