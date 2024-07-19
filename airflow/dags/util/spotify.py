import base64
import os
from typing import List

import requests


class SpotifyAPI:
    def __init__(self):
        self.client_id = os.environ.get('SPOTIFY_CLIENT_ID')
        self.client_secret = os.environ.get('SPOTIFY_SECRET')

    def __auth(self) -> str:
        auth_url = 'https://accounts.spotify.com/api/token'
        auth_header = base64.b64encode(f"{self.client_id}:{self.client_secret}".encode()).decode()
        headers = {'Authorization': f'Basic {auth_header}'}
        data = {'grant_type': 'client_credentials'}
        response = requests.post(auth_url, headers=headers, data=data)
        response_data = response.json()
        return response_data['access_token']

    def get_top_songs_recommendation(self, genre: str) -> dict:
        token = self.__auth()
        api_url = f'https://api.spotify.com/v1/recommendations'
        headers = {'Authorization': f'Bearer {token}'}
        params = {'seed_genres': genre, 'market': 'BR', 'min_popularity': 40, 'limit': 100}
        response = requests.get(api_url, headers=headers, params=params)
        return response.json()
    
    def get_available_genres(self) -> List[str]:
        token = self.__auth()
        print("token", token)
        api_url = f'https://api.spotify.com/v1/recommendations/available-genre-seeds'
        headers = {'Authorization': f'Bearer {token}'}
        response = requests.get(api_url, headers=headers)
        return response.json()

if __name__ == '__main__':
    
    spotifyApi = SpotifyAPI()
    genres = spotifyApi.get_top_songs_recommendation('sad')
    print(genres)
    