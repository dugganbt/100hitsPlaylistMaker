import requests
from dotenv import load_dotenv
import base64
import os

path = os.path.join("Web scraping projects", "100hitsPlaylistMaker")

# load environment variables for API
load_dotenv(os.path.join(path,".env"))

user_id = os.getenv("user_id")
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")

def get_access_token(client_id=client_id, client_secret=client_secret):

    # Encode the client ID and client secret
    auth_str = f'{client_id}:{client_secret}'
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    # Set up the request headers and body
    headers = {
        'Authorization': f'Basic {b64_auth_str}',
        "Content-Type":"application/x-www-form-urlencoded"
    }
    data = {
        'grant_type': 'client_credentials'
    }

    # Make the request to get the access token
    response = requests.post('https://accounts.spotify.com/api/token', headers=headers, data=data)
    return response.json()['access_token']

def create_spotify_playlist_for_date(date, user_id=user_id):

    create_playlist_endpoint = f"https://api.spotify.com/v1/users/{user_id}/playlists"

    access_token = get_access_token()
    print(access_token)

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
        'name': "100 Top Hits for {date}",
        'description': "100 Top Hits for {date}",
        'public': True
    }

    response = requests.post(f'https://api.spotify.com/v1/users/{user_id}/playlists', headers=headers, json=data)
    playlist_info = response.json() 

    print(playlist_info)



create_spotify_playlist_for_date("1996-05-10")