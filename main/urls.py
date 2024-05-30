from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_games, name='search'),
    path('details/', views.details, name='details'),
]
