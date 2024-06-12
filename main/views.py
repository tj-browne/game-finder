import os

from django.contrib.sites import requests
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
            client_id = form.cleaned_data['client_id']
            access_token = form.cleaned_data['access_token']

            # Attempt to make a request to the API using the provided credentials
            api_url = 'ttps://api.igdb.com/v4'
            headers = {'Authorization': f'Bearer {access_token}', 'Client-ID': client_id}
            response = requests.get(api_url, headers=headers)

            if response.status_code == 200:
                # Credentials are valid, process them accordingly
                return redirect('search')  # Redirect to a success page
            else:
                # Credentials are invalid, display an error message
                error_message = "Invalid client ID or access token."
                try:
                    error_response = response.json()
                    if 'error' in error_response:
                        error_message = error_response['error']
                except ValueError:
                    pass  # Ignore if response is not JSON
                form.add_error(None, error_message)
    else:
        form = CredentialsForm()
    return render(request, 'main/credentials.html', {'form': form, 'referer': referer})
