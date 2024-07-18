from django.urls import path
from . import views

app_name = "rank"

urlpatterns = [
    path("list/", list, name = "list"),
]