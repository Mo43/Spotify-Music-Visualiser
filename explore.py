import json
import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("REDIRECT_URI"),
    scope="user-top-read user-read-recently-played",
))

recent = sp.current_user_recently_played(limit=5)

for item in recent['items']:
    print(f"{item['played_at']} | {item['track']['name']} | {item['track']['album']['name']} | {item['track']['artists'][0]['name']}")

#print(json.dumps(recent['items'][0], indent=2))