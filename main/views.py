import os

from django.shortcuts import render

from .api_service import apiService


def home(request):
    return render(request, 'main/search.html')


def search_games(request):
    query = request.GET.get('query')
    games = []
    if query:
        client_id = os.getenv('CLIENT_ID')
        access_token = os.getenv('ACCESS_TOKEN')
        api = apiService(client_id, access_token)
        games = api.get_games(query)

    return render(request, 'main/search.html', {'games': games})


def get_game_details(request, game_id):
    client_id = os.getenv('CLIENT_ID')
    access_token = os.getenv('ACCESS_TOKEN')
    api = apiService(client_id, access_token)
    game_details = api.get_game_details(game_id)
    referer = request.META.get('HTTP_REFERER', '/')

    return render(request, 'main/details.html', {'game_details': game_details, 'referer': referer})
