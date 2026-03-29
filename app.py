import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import session, redirect, request
from flask import Flask, render_template
import sqlite3
from dotenv import load_dotenv
load_dotenv()
print("REDIRECT_URI:", os.getenv("REDIRECT_URI"))
from database import setup_database


app = Flask(__name__)
app.secret_key = "your_secret_key"

client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
redirect_uri =os.getenv("REDIRECT_URI")

if not client_id or not client_secret or not redirect_uri:
    raise ValueError("Missing Spotify environment variables")

sp_oauth = SpotifyOAuth(
    client_id = client_id,
    client_secret = client_secret,
    redirect_uri = redirect_uri,
    scope = "user-top-read",
    cache_handler=None
)
def ms_to_minutes(ms):
    if ms is None:
        return "Unknown"
    minutes = ms // 60000
    seconds = (ms%60000) // 1000
    return f"{minutes}:{seconds:02d}"


@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url+ "&show_dialog=true")


@app.route('/callback')
def callback():
    code = request.args.get('code')
    session.clear()
    token_info = sp_oauth.get_access_token(code,as_dict=True)
    session['access_token'] = token_info.get('access_token')
    return redirect('/')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/')
def home():
    token = session.get('access_token')
    
    if not token:
        return redirect ('/login')
    if token:
        sp = spotipy.Spotify(auth=token)
        top_tracks = sp.current_user_top_tracks(limit=10)
        setup_database()
        print(sp.current_user()['display_name'])
        
        conn = sqlite3.connect("music.db")
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM tracks")
        for item in top_tracks['items']:
            cursor.execute("""
                        INSERT INTO tracks (id, name, artist, albums, duration_ms, popularity)
                VALUES (?, ?, ?, ?, ?,?)""",(
                item['id'],
                item['name'],
                item['artists'][0]['name'],
                item['album']['name'],
                item['duration_ms'],
                item.get('popularity', 0)
                ))
        conn.commit()
        conn.close()
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, artist, albums, duration_ms, popularity FROM tracks")
    songs = cursor.fetchall()
    # longest track
    longest = max(songs, key=lambda s: (s[4] or 0)) if songs else None
    insight = (
f" {longest[1]} ({ms_to_minutes(longest[4])})"        if longest else
        "No tracks found yet."
    )
    
    # avg duration
    if songs:
        total_ms  = sum((s[4]or 0) for s in songs)
        avg_ms = total_ms // len(songs)
        average_insight =f" {ms_to_minutes(avg_ms)}"
    else:
        average_insight = ""
        
    conn.close()
    converted_songs = [(s[0],s[1], s[2], s[3], ms_to_minutes(s[4])) for s in songs] 
    return render_template('index.html', songs = converted_songs, insight=insight,average_insight=average_insight,)

@app.route('/artists')
def artists():
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()
    cursor.execute ("SELECT id, name, genres, popularity, followers from artists")
    artists = cursor.fetchall()
    count = len(artists)
    artists_insight = (
    f"You have {count} top artists."
    if count
    else "No artists found."
)
    conn.close()
    return render_template('artists.html', artists=artists, artists_insight = artists_insight)

if __name__ == "__main__":
    app.run(debug=True)




