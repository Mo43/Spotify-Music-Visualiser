from database import setup_database, save_tracks
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os


load_dotenv() # function from dotenv that does the reading

sp = spotipy.Spotify(auth_manager = SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"), # connected to spotify app
    redirect_uri=os.getenv("REDIRECT_URI"),
    scope="user-top-read"
))

results = sp.current_user_top_tracks(limit=10)

track_ids = [track['id'] for track in results['items']]
full_tracks = sp.tracks(track_ids)

for i, track in enumerate(full_tracks['tracks']):
    results['items'][i]['popularity'] = track['popularity']


for i, track in enumerate(results['items']):
    #print(track)
    print(i+1, track['name'], "by", track['artists'][0]['name'])

    
    
setup_database()
save_tracks(results)
