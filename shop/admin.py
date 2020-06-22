from django.contrib import admin
from .models import Category, Product, ShippingCosts


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'weight',
                    'available', 'created', 'updated', 'priority']
    list_filter = ['category', 'available', 'created', 'updated', 'priority']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ShippingCosts)
class ShippingCostsAdmin(admin.ModelAdmin):
    list_display = ['min_weight', 'max_weight', 'price']
