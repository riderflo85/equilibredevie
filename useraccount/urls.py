from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = "useraccount"
urlpatterns = [
    path('login/', views.login_user, name="login"),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='useraccount/login.html'),
        name="logout"
    ),
    path('register/', views.register, name="register"),
    path('', views.account, name="account"),
]
