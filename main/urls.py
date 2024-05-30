from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_games, name='search'),
    path('details/<int:game_id>/', views.get_game_details, name='details'),
]
