import requests


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

    def search_games(self, query):
        url = f"{self.base_url}/games"
        headers = self.get_headers()
        data = f'search "{query}"; fields name, cover.url, cover.image_id, id; limit 10;'
        response = requests.post(url, headers=headers, data=data)
        response.raise_for_status()
        return response.json()

    # Search images (requires id of image from game)

    # Search game details (name, description, release date, genres, platforms, Developer, Publisher, (Large game cover))
    # (requires id of game???)
    # def game_details(self, query):
    #     url = f"{self.base_url}/games"
    #     headers = self.get_headers()
    #     data = f'search "{query}"; fields name, summary, release_dates, genres, platforms, involved_companies;'
    #     response = requests.post(url, headers=headers, data=data)
    #     response.raise_for_status()
    #     return response.json()
