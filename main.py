from database import setup_database, save_tracks, setup_artists_table, save_artists
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),
    scope="user-top-read"
))

results = sp.current_user_top_tracks(limit=10)
artist_results = sp.current_user_top_artists(limit=10)
for i, track in enumerate(results['items']):
    print(i+1, track['name'], "by", track['artists'][0]['name'])

for i, artist in enumerate(artist_results['items']):
    print(i+1, artist['name'])
setup_database()
save_tracks(results)
setup_artists_table()
save_artists(artist_results)