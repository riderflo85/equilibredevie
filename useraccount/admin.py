from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'last_name',
        'first_name',
        'username',
        'date_joined',
        'email',
        'civility',
        'phone_number',
        'adress',
        'postal_code',
        'city',
        'is_verified',
    ]