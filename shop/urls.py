from django.urls import path
from . import views

app_name = "shop"

urlpatterns = [
    path('', views.ProductsListView.as_view(), name="shop"),
    path('product_detail/<int:id>', views.product_detail, name="product_detail"),
]
