from django.contrib.auth import views as auth_views
from django.urls import path
from . import views


app_name = "user"
urlpatterns = [
    path('login/', views.login_user, name="login"),
    path(
        'logout/',
        auth_views.LogoutView.as_view(template_name='user/login.html'),
        name="logout"
    ),
]
