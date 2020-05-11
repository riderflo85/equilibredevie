from django.urls import path
from . import views

app_name = "cart"

urlpatterns = [
    path('', views.index_cart, name="cart"),
    path('add/<int:product_id>/', views.add_product_in_cart, name="cart_add"),
    path(
        'remove/<int:product_id>/',
        views.remove_product_in_cart,
        name="cart_remove"
    ),
    path('update/', views.update_cart, name="cart_update"),
]
