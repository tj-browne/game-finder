import requests


def get_covers(game, size='t_cover_big'):
    if 'cover' in game and 'url' in game['cover']:
        game['cover']['url'] = game['cover']['url'].replace('t_thumb', size)
    # if 'screenshots' in game:
    #     for screenshot in game['screenshots']:
    #         if 'url' in screenshot:
    #             screenshot['url'] = screenshot['url'].replace('t_thumb', size)


# TODO: (API Access Token)
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
        data = f'search "{query}"; fields name, cover.url, id; limit 10;'
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
