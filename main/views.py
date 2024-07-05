import os

import requests
from django.conf import settings

from django.shortcuts import render, redirect

from .api_service import apiService
from .forms import CredentialsForm


def home(request):
    return render(request, 'main/search.html')


def search_games(request):
    # if not request.session.get('client_id') or not request.session.get('client_secret') or not settings.CLIENT_ID or not settings.CLIENT_SECRET:
    #     return redirect('credentials')

    query = request.GET.get('query')
    error_message = None
    games = []
    if query:
        try:
            api = apiService(request)
            games = api.get_games(query)
        except KeyError as e:
            print(f"KeyError: {e}")
            error_message = "Error fetching games. Please try again later or check API credentials."
        except Exception as e:
            # API request errors
            print(f"Error: {e}")
            error_message = "Error fetching games. Please try again later or check API credentials."

    return render(request, 'main/search.html', {'games': games, 'error_message': error_message})


def get_game_details(request, game_id):
    api = apiService(request)
    game_details = api.get_game_details(game_id)
    referer = request.META.get('HTTP_REFERER', '/')

    return render(request, 'main/details.html', {'game_details': game_details, 'referer': referer})


def set_credentials(request):
    referer = request.META.get('HTTP_REFERER', '/')
    error_message = None
    if request.method == 'POST':
        form = CredentialsForm(request.POST)
        if form.is_valid():
            request.session['client_id'] = form.cleaned_data['client_id']
            # request.session['access_token'] = form.cleaned_data['access_token']
            request.session['client_secret'] = form.cleaned_data['client_secret']
            try:
                # Initialize apiService with the provided credentials
                api = apiService(request)

                # Authenticate to get the access token
                api.authenticate()

                # Store the access token in the session if authentication is successful
                request.session['access_token'] = api.access_token
                return redirect('search')
            except requests.exceptions.HTTPError:
                # Extract error message
                error_message = "Failed to authenticate. Check client credentials."
            except TypeError:
                error_message = "Failed to authenticate. Check client credentials."

    else:
        form = CredentialsForm()
    return render(request, 'main/credentials.html', {'form': form, 'referer': referer, 'error_message': error_message})
