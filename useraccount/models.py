from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from shop.models import Order


USER_CIVILITY = [
    ('Mr', 'Monsieur'),
    ('Mme', 'Madame')
]

class User(AbstractUser):
    email = models.EmailField(
        _('adresse email'),
        null=False,
        unique=True
    )
    civility = models.CharField(
        max_length=8,
        null=False,
        choices=USER_CIVILITY,
        verbose_name='Civilité'
    )
    phone_number = models.IntegerField(
        null=False,
        verbose_name='Numéro de téléphone'
    )
    adress = models.CharField(
        max_length=350,
        null=False,
        verbose_name='Adresse'
    )
    postal_code = models.IntegerField(
        null=False,
        verbose_name='Code postale'
    )
    city = models.CharField(
        max_length=250,
        null=False,
        verbose_name='Ville'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Compte vérifié'
    )
    order = models.ManyToManyField(Order)

    def __str__(self):
        return f"{self.civility} {self.last_name} {self.first_name}"
