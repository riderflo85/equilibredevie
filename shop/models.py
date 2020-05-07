from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(
        max_length=200, db_index=True, verbose_name="Nom de la categorie"
    )
    slug = models.SlugField(
        max_length=200, unique=True, verbose_name="Étiquette"
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'categorie'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])


PRIORITY = [
    ('1', '*****'),
    ('2', '****'),
    ('3', '***'),
    ('4', '**'),
    ('5', '*')
]


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        related_name='products',
        on_delete=models.CASCADE,
        verbose_name="Categorie"
    )
    name = models.CharField(
        max_length=200, db_index=True, verbose_name="Nom du produit"
    )
    slug = models.SlugField(
        max_length=200, db_index=True, verbose_name="Étiquette"
    )
    image_home = models.ImageField(
        upload_to='products/home/%Y/%m/%d',
        blank=True,
        verbose_name="Image 320x360"
    )
    image_shop = models.ImageField(
        upload_to='products/shop/%Y/%m/%d',
        blank=True,
        verbose_name="Image 312x400"
    )
    image_detail_s = models.ImageField(
        upload_to='products/detail_s/%Y/%m/%d',
        blank=True,
        verbose_name="Image 125x156"
    )
    image_detail_m = models.ImageField(
        upload_to='products/detail_m/%Y/%m/%d',
        blank=True,
        verbose_name="Image 500x654"
    )
    image_detail_l = models.ImageField(
        upload_to='products/detail_l/%Y/%m/%d',
        blank=True,
        verbose_name="Image 1200x1125"
    )
    image_cart = models.ImageField(
        upload_to='products/cart/%Y/%m/%d',
        blank=True,
        verbose_name="Image 85x101"
    )
    description = models.TextField(blank=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Prix TTC"
    )
    available = models.BooleanField(
        default=True, verbose_name="Rendre publique"
    )
    priority = models.CharField(
        max_length=5,
        choices=PRIORITY,
        verbose_name='ordre de priorité'
    )
    created = models.DateTimeField(
        auto_now_add=True, verbose_name="Créer le"
    )
    updated = models.DateTimeField(
        auto_now=True, verbose_name="Mis à jour la"
    )

    class Meta:
        ordering = ('priority', 'name')
        verbose_name = "Produit"
        verbose_name_plural = 'Produits'
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])


class Order(models.Model):
    reference = models.CharField(
        max_length=50, verbose_name='Référence de la commande'
    )


class ProductQuantity(models.Model):
    id_product = models.ForeignKey(Product, on_delete=models.CASCADE)
    id_order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, verbose_name='Quantité')
