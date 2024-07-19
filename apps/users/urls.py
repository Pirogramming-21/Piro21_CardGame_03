from django.urls import path, include
from . import views

app_name = "users"

urlpatterns = [
    path("", views.main, name = "main"),
    path("signup/", views.signup, name = "signup"),
    path("login/", views.login, name = "login"),
    path("logout/", views.logout, name = "logout"),
    path("accounts/", include("allauth.urls")),
]