from django.db import models


class NewsLetter(models.Model):
    title = models.CharField(
        max_length=50,
        verbose_name='titre de la newsletter'
    )
    body = models.TextField(verbose_name='contenu de la newsletter')
    send = models.BooleanField(verbose_name='envoyé', default=False)
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name='créer le'
    )
    updated = models.DateTimeField(
        auto_now=True,
        verbose_name='mis à jour le'
    )

    class Meta:
        ordering = ('created',)
        verbose_name = 'newsletter'
        verbose_name_plural = 'newsletters'

    def __str__(self):
        return f"Newsletter du {self.created}"
