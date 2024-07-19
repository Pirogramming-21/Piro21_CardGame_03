from django.urls import path
from . import views

app_name = "rank"

urlpatterns = [
    path("list/", views.ranking, name = "ranking"),
]