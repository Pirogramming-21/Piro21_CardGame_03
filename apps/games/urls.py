from django.urls import path
from . import views

app_name = "games"

urlpatterns = [
    path("attack/", views.attack, name="attack"),
    path("list/", views.game_list, name="list"),
    path("counter_attack/<int:pk>/", views.counter_attack, name="counter_attack"),
    path('cancel/<int:pk>/', views.game_cancel, name='cancel'),
    path('detail/<int:pk>/', views.game_detail, name='detail'),
]