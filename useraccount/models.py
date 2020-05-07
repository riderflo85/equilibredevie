from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from shop.models import Order


class User(AbstractUser):
    email = models.EmailField(
        _('adresse email'),
        null=False,
        unique=True
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
        return f"{self.first_name} {self.last_name}"