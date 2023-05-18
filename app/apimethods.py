import requests
import base64
import json
import urllib

# Spotify API
SPOTIFY_API_BASE_URL = 'https://api.spotify.com/v1'
SPOTIFY_CLIENT_ID = '7e8682088ce94ba4b6599a96fa11129b'
SPOTIFY_CLIENT_SECRET = 'e68b36407b4a4cb9ad14c3ea756076fd'

# YouTube Data API
YOUTUBE_API_BASE_URL = 'https://www.googleapis.com/youtube/v3/'
YOUTUBE_API_KEY = 'AIzaSyD4Xwq5Dxz8dHs6ULSzoULdO9meYnN9F2Q'

# Get Spotify access token
def get_token():
    auth_string = SPOTIFY_CLIENT_ID + ":" + SPOTIFY_CLIENT_SECRET
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    response = requests.post(url, headers=headers, data=data)
    json_result = response.json()

    token = json_result["access_token"]
    return token

# Get top 10 songs from Spotify
def get_top_songs():
    access_token = get_token()
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.get(f'{SPOTIFY_API_BASE_URL}/playlists/37i9dQZEVXbMDoHDwVN2tF', headers=headers)  # 37i9dQZEVXbMDoHDwVN2tF is the id for Global Top 50
    data = response.json()

    return data['tracks']['items']


