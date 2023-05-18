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


def search_youtube_video(artist, song_name):
    # Format the search query
    query = f'{artist} {song_name}'
    query_encoded = urllib.parse.quote(query)

    # Construct the API request URL
    url = f'{YOUTUBE_API_BASE_URL}search?part=snippet&type=video&q={query_encoded}&key={YOUTUBE_API_KEY}'

    # Send the request to the API
    response = requests.get(url)
    data = response.json()

    # Check for errors in the API response
    if 'error' in data:
        error_message = data['error']['message']
        print(f"YouTube API Error: {error_message}")
        return None

    # Extract the video link from the API response
    if 'items' in data and len(data['items']) > 0:
        video_id = data['items'][0]['id']['videoId']
        video_link = f'https://www.youtube.com/watch?v={video_id}'
        return video_link

    return None

# Format the output and display the results
def format_output(songs):
    print("Top 10 Songs:")
    print("-----------------------------")
    for i, song in enumerate(songs, 1):
        name = song['track']['name']
        artist = song['track']['artists'][0]['name']
        video_link = search_youtube_video(artist, name)
        
        print(f"{i}. {name} - {artist}")
        if video_link:
            print(f"YouTube Video Link: {video_link}")
        else:
            print("No YouTube video found for this song.")
        print("-----------------------------")


# Format the output and display the results
def format_output(songs):
    print("Top 10 Songs:")
    print("-----------------------------")
    for i, song in enumerate(songs, 1):
        name = song['track']['name']
        artist = song['track']['artists'][0]['name']
        video_link = search_youtube_video(artist, name)

        print(f"{i}. {name} - {artist}")
        if video_link:
            print(f"YouTube Video Link: {video_link}")
        else:
            print("No YouTube video found for this song.")
        print("-----------------------------")

# Format the output and display the results
def format_output(songs):
    print("Top 50 Songs:")
    print("-----------------------------")
    for i, song in enumerate(songs, 1):
        name = song['track']['name']
        artist = song['track']['artists'][0]['name']
        video_link = search_youtube_video(artist, name)

        print(f"{i}. {name} - {artist}")
        if video_link:
            print(f"YouTube Video Link: {video_link}")
        else:
            print("No YouTube video found for this song.")
        print("-----------------------------")



def get_video_statistics(video_link):
    # Extract the video ID from the link
    video_id = extract_video_id(video_link)


    if video_id:
        # Construct the API request URL
        url = f'{YOUTUBE_API_BASE_URL}videos?part=statistics&id={video_id}&key={YOUTUBE_API_KEY}'


        # Send the request to the API
        response = requests.get(url)
        data = response.json()


        # Extract and return the video statistics
        if 'items' in data and len(data['items']) > 0:
            statistics = data['items'][0]['statistics']
            return statistics


    return None


def extract_video_id(video_link):
    # Extract the video ID from the link
    video_id = None
    if 'youtube.com/watch?v=' in video_link:
        video_id = video_link.split('youtube.com/watch?v=')[1].split('&')[0]
    elif 'youtu.be/' in video_link:
        video_id = video_link.split('youtu.be/')[1].split('?')[0]
    return video_id



# Format the output and display the results
def format_output(songs):
    print("Top 50 Songs:")
    print("-----------------------------")
    for i, song in enumerate(songs, 1):
        name = song['track']['name']
        artist = song['track']['artists'][0]['name']
        video_link = search_youtube_video(artist, name)

        print(f"{i}. {name} - {artist}")
        if video_link:
            print(f"YouTube Video Link: {video_link}")
            statistics = get_video_statistics(video_link)
            if statistics:
                print("Video Statistics:")
                print(f"Views: {statistics.get('viewCount', 'N/A')}")
                print(f"Likes: {statistics.get('likeCount', 'N/A')}")
                print(f"Dislikes: {statistics.get('dislikeCount', 'N/A')}")
                print(f"Comments: {statistics.get('commentCount', 'N/A')}")
        else:
            print("No YouTube video found for this song.")
        print("-----------------------------")


# Get top songs from Spotify
top_songs = get_top_songs()

# Format and display the combined output
format_output(top_songs)
