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

    def get_all_products_without_declination(self):
        return self.products.all().exclude(is_a_declination=True)


class Product(models.Model):
    PRIORITY = [
        ('1', '*****'),
        ('2', '****'),
        ('3', '***'),
        ('4', '**'),
        ('5', '*')
    ]
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
    weight = models.PositiveIntegerField(
        verbose_name="Poids en Kilos"
    )
    size = models.CharField(
        max_length=5,
        blank=True,
        verbose_name="Taille du produit (exemple: S, M, L, XL...)"
    )
    dimension = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Dimension du produit (exemple: 110x200cm)"
    )
    color = models.CharField(
        max_length=50,
        blank=True,
        verbose_name="Couleur du produit"
    )
    liter_capacity = models.PositiveIntegerField(
        blank=True,
        verbose_name="Contenance en Litre"
    )
    has_a_declination = models.BooleanField(
        verbose_name="Le produit À une déclinaison ?",
        default=False
    )
    is_a_declination = models.BooleanField(
        verbose_name="Le produit EST une déclinaison ?",
        default=False
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
        auto_now=True, verbose_name="Mis à jour le"
    )


    class Meta:
        ordering = ('priority', 'name')
        verbose_name = "Produit"
        verbose_name_plural = 'Produits'
        # index_together = (('id', 'slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id])


class ShippingCosts(models.Model):
    min_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Poids minimum pour frais de port"
    )
    max_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Poids maximum pour frais de port"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Prix de frais de port TTC"
    )

    class Meta:
        verbose_name = "Frais de port"

    def __str__(self):
        return f"De {self.min_weight} à {max_weight}, \
        les frais de port sont de {self.price}"


class ProductDeclination(models.Model):
    TYPE_OF_DECLINATION = [
        ('weight', 'Poid'),
        ('size', 'Taille'),
        ('dimension', 'Dimension'),
        ('color', 'Couleur'),
        ('liter_capacity', 'Litre'),
    ]
    original_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="FK_ProductDeclination_original_product",
        verbose_name="Produit original"
    )
    declined_product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="FK_ProductDeclination_declined_product",
        verbose_name="Produit décliné"
    )
    type_of_declination = models.CharField(
        max_length=150,
        choices=TYPE_OF_DECLINATION,
        verbose_name="type de déclinaison (exemple: poid, couleur, taille...)"
    )

    class Meta:
        verbose_name = "Déclinaison de produit"
        verbose_name_plural = "Déclinaison de produits"
