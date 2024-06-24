import requests
from dotenv import load_dotenv
import base64
import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from billboard_scraper import scrape_100_hits_for_date

path = os.path.join("Web scraping projects", "100hitsPlaylistMaker")

# load environment variables for API
load_dotenv(os.path.join(path,".env"))

user_id = os.getenv("user_id")
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_url = os.getenv("redirect_url")

def get_song_url(sp, song, year, artist):
    max_attempts = 5
    attempts = 0

    # Allow the search for the song in the previous 5 years
    while attempts < max_attempts:
        query = f"track:{song} artist:{artist} year:{year}"
        result = sp.search(q=query, type='track', limit=1)
        
        try:
            uri = result["tracks"]["items"][0]["uri"]
            return uri
        except IndexError:
            attempts += 1
            year = str(int(year) - 1)  # Decrease the year by 1 and convert it back to a string
            
    # If no results found after max_attempts
    print(f"{song} by {artist} not found in Spotify after {max_attempts} attempts.")
        

def create_spotify_playlist_for_date(date, client_id=client_id, client_secret=client_secret, 
                                     redirect_url=redirect_url):
    #Spotify client setup
    scope = "playlist-modify-public" # public playlist
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                                client_secret=client_secret,
                                                redirect_uri=redirect_url,
                                                scope=scope))

    # create the playlist
    results = sp.user_playlist_create(user=user_id,name=f"Top 100 Hits for {date}")
    playlist_id = results['id']
    print(f"Created playlist: Top 100 Hits for {date}")

    # Get track list from billboard
    track_list = scrape_100_hits_for_date(date=date)

    # Create a list of spotify urls for each song
    track_urls = []
    year = date[0:4]
    for track in track_list:
        song_name, artist = track
        song_url = get_song_url(sp, song_name, year, artist)
        if song_url is not None:
            track_urls.append(song_url)

    # Add each song to the playlist
    sp.user_playlist_add_tracks(user=user_id, playlist_id=playlist_id, tracks=track_urls)
