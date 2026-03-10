from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def ms_to_minutes(ms):
    if ms is None:
        return "Unknown"
    minutes = ms // 60000
    seconds = (ms%60000) // 1000
    return f"{minutes}:{seconds:02d}"

@app.route('/')
def home():
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, artist, albums, duration_ms, popularity FROM tracks")
    songs = cursor.fetchall()
    conn.close()
    converted_songs = [(s[0],s[1], s[2], ms_to_minutes(s[3]),s[4]) for s in songs]
    return render_template('index.html', songs = converted_songs)

@app.route('/artists')
def artists():
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()
    cursor.execute ("SELECT name, genres, popularity, followers from artists")
    artists = cursor.fetchall()
    conn.close()
    return render_template('artists.html', artists=artists)



if __name__ == "__main__":
    app.run(debug=True)

