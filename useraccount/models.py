import random, string
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from order.models import Order


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
    newsletter = models.BooleanField(
        default=False,
        verbose_name='abonnement newsletter'
    )
    is_verified = models.BooleanField(
        default=False,
        verbose_name='Compte vérifié'
    )
    activate_key = models.CharField(
        max_length=48,
        blank=True,
        verbose_name="Clé de vérification d'email"
    )
    check_code = models.CharField(
        max_length=10,
        default="nill",
        verbose_name="Code de réinitialisation de mot de passe"
    )
    order = models.ManyToManyField(Order)

    def __str__(self):
        return f"{self.civility} {self.last_name} {self.first_name}"

    def generate_activate_key(self):
        """
        Create a random key for check the user email.
        """

        for_key = string.ascii_letters + string.digits

        self.activate_key = "".join(random.choice(for_key) for _ in range(48))
        self.save()

    def generate_check_code_reset_password(self):
        """
        Create a random code for the user can change his password.
        """

        code = string.ascii_uppercase + string.digits

        self.check_code = "".join(random.choice(code) for _ in range(10))
        self.save()