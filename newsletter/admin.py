from django.contrib import admin
from .models import NewsLetter


@admin.register(NewsLetter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ['title', 'body', 'send', 'created', 'updated']
