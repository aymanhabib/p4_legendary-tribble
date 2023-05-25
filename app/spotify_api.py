import os
import base64
from requests import post, get
import json

client_id = "7e8682088ce94ba4b6599a96fa11129b"
client_secret = "e68b36407b4a4cb9ad14c3ea756076fd"

# print(client_id, client_secret)

def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result[0]

def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    songs = getTop10(json_result)
    return songs

Top10Songs = {}
def getTop10(songs):
    Top10String = f""
    for idx, song in enumerate(songs):
        Top10String+= f"{idx + 1}. {song['name']} \n"
        rank = idx + 1
        songName = song['name']
        Top10Songs[songName] = song
    return Top10String


"""
token = get_token()
artist_name = input("Enter desired artist: ")
result = search_for_artist(token, artist_name)
artist_id = result["id"]
songs = get_songs_by_artist(token, artist_id)

Top10Songs = {}
for idx, song in enumerate(songs):
    # print(song)
    print(f"{idx + 1}. {song['name']}")
    rank = idx + 1
    songName = song['name']
    Top10Songs[songName] = song
  """

# for song in Top10Songs:
   # print(song)
   # print(Top10Songs[song]['name'])
   # print(Top10Songs[song]['id'])

#title = input("Enter desired track name (Case sensitive): ")
# print(Top10Songs)

def get_song_features(token, title):
    track_id = Top10Songs[title]['id']
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)
    return(get_chart_data(json_result))

def get_chart_data(data):
    song_data = {}
    song_data['danceability'] = data['danceability']
    song_data['energy'] = data['energy']
    song_data['acousticness'] = data['acousticness']
    song_data['speechiness'] = data['speechiness']
    song_data['liveness'] = data['liveness']
    song_data['instrumentalness'] = data['instrumentalness']
    song_data['valence'] = data['valence']
    return song_data

