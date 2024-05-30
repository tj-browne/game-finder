import os

from django.shortcuts import render

from .api_service import apiService


# Create your views here.
def home(request):
    return render(request, 'main/search.html')


def search_games(request):
    query = request.GET.get('query')
    games = []
    if query:
        client_id = os.getenv('CLIENT_ID')
        access_token = os.getenv('ACCESS_TOKEN')
        api = apiService(client_id, access_token)
        games = api.search_games(query)

    return render(request, 'main/search.html', {'games': games})


def details(request):
    return render(request, 'main/details.html')
