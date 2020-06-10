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
    path('change_pwd/', views.change_pwd, name="change_password"),
    path('change_infos/', views.change_user_infos, name="change_infos"),
    path('active_account', views.active_account, name="activation"),
    path('forgot_password/', views.forgot_password, name="forgot_password"),
    path('reset_password/', views.reset_password, name="reset_password"),
    path(
        'success_reset_pwd/',
        views.success_reset_pwd,
        name="success_reset_pwd"
    ),
]
