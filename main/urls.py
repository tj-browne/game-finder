from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_games, name='home'),
    path('details/', views.details),
]
