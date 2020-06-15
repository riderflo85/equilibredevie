from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.list_all_products, name="shop"),
    path(
        'product_detail/<int:id_item>',
        views.product_detail,
        name="product_detail"
    ),
]
