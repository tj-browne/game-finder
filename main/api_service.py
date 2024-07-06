import requests
from django.conf import settings


def get_covers(game, size='t_cover_big'):
    if 'cover' in game and 'url' in game['cover']:
        game['cover']['url'] = game['cover']['url'].replace('t_thumb', size)


class apiService:

    def __init__(self, request):
        self.client_id = settings.CLIENT_ID
        self.client_secret = settings.CLIENT_SECRET
        try:
            self.access_token = request.session['access_token']
        except KeyError:
            self.authenticate()
            request.session['access_token'] = self.access_token
        self.base_url = 'https://api.igdb.com/v4'

    def authenticate(self):
        auth_url = 'https://id.twitch.tv/oauth2/token'
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(auth_url, data=data)
        response.raise_for_status()
        response_data = response.json()

        if 'access_token' in response_data:
            self.access_token = response_data['access_token']
        else:
            raise ValueError("Failed to authenticate. Check client credentials.")

    def get_headers(self):
        return {
            "Client-ID": self.client_id,
            "Authorization": f"Bearer {self.access_token}",
        }

    def get_request(self, data, endpoint='games'):
        url = f"{self.base_url}/{endpoint}"
        headers = self.get_headers()
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    def get_games(self, query):
        data = f'search "{query}"; fields name, cover.url, id; limit 20;'
        games = self.get_request(data)
        for game in games:
            get_covers(game)
        return games

    def get_game_details(self, game_id):
        data = (f'fields name, summary, release_dates.human, genres.name, platforms.name, '
                f'involved_companies.company.name, cover.url, cover.image_id, id; where id = {
                game_id};')
        game_details = self.get_request(data)
        game_details = game_details[0]
        get_covers(game_details, 't_cover_big_2x')
        return game_details
