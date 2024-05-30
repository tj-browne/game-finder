import requests


def get_covers(games, size='t_cover_big'):
    for game in games:
        if 'cover' in game and 'url' in game['cover']:
            if 't_thumb' in game['cover']['url']:
                game['cover']['url'] = game['cover']['url'].replace('t_thumb', size)


# TODO: Get Release Dates
def get_release_dates(game_details):
    pass


# TODO: Get Genres
def get_genres(game_details):
    pass


# TODO: Get Platforms
def get_platforms(game_details):
    pass


# TODO: Get Involved Companies
def get_companies(game_details):
    pass


class apiService:
    def __init__(self, client_id, access_token):
        self.client_id = client_id
        self.access_token = access_token
        self.base_url = 'https://api.igdb.com/v4'

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
        data = f'search "{query}"; fields name, cover.url, cover.image_id, id; limit 10;'
        games = self.get_request(data)
        get_covers(games)
        return games

    def get_game_details(self, game_id):
        data = f'fields name, summary, release_dates, genres, platforms, involved_companies, cover.url, cover.image_id, id; where id = {game_id};'
        game_details = self.get_request(data)
        get_covers(game_details, 't_cover_big_2x')
        return game_details
