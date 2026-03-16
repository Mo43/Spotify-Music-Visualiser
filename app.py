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




