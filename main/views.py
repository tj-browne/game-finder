import os

from django.shortcuts import render, redirect

from .api_service import apiService
from .forms import CredentialsForm


def home(request):
    return render(request, 'main/search.html')


def search_games(request):
    if not request.session.get('client_id') or not request.session.get('access_token'):
        return redirect('credentials')

    query = request.GET.get('query')
    games = []
    if query:
        api = apiService(request)
        games = api.get_games(query)

    return render(request, 'main/search.html', {'games': games})


def get_game_details(request, game_id):
    api = apiService(request)
    game_details = api.get_game_details(game_id)
    referer = request.META.get('HTTP_REFERER', '/')

    return render(request, 'main/details.html', {'game_details': game_details, 'referer': referer})


def set_credentials(request):
    referer = request.META.get('HTTP_REFERER', '/')
    if request.method == 'POST':
        form = CredentialsForm(request.POST)
        if form.is_valid():
            request.session['client_id'] = form.cleaned_data['client_id']
            request.session['access_token'] = form.cleaned_data['access_token']
            return redirect('search')
    else:
        form = CredentialsForm()
    return render(request, 'main/credentials.html', {'form': form, 'referer': referer})
