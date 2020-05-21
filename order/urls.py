from django.urls import path
from . import views

app_name = "order"

urlpatterns = [
    path('', views.create_order, name="create_order"),
    path('success', views.success_order, name="successorder"),
    path('error', views.fail_order, name="failorder"),
    path('test', views.test_view, name='test'),
]
