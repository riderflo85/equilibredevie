from django.contrib import admin
from .models import Category, Product, ShippingCosts, ProductDeclination


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'weight', 'category',
                    'available', 'created', 'updated',
                    'priority', 'has_a_declination', 'is_a_declination'
                    ]
    list_filter = ['category', 'available', 'created', 'updated', 'priority']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(ShippingCosts)
class ShippingCostsAdmin(admin.ModelAdmin):
    list_display = ['min_weight', 'max_weight', 'price']


@admin.register(ProductDeclination)
class ProductDeclinationAdmin(admin.ModelAdmin):
    list_display = ['original_product', 'declined_product']
