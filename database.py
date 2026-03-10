import sqlite3

def setup_database():
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS tracks(
        id TEXT PRIMARY KEY,
        name TEXT,
        artist TEXT,
        albums TEXT,
        duration_ms INTEGER,
        popularity INTEGER
    )
    ''')
    conn.commit()
    conn.close()
       
def save_tracks(results):
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()
    
    for track in results['items']:
        cursor.execute('''
    INSERT OR IGNORE INTO tracks (id, name, artist, albums, duration_ms, popularity)
    VALUES (?, ?, ?, ?, ?, ?)
''', (
    track.get('id'),
    track.get('name'),
    track['artists'][0]['name'],
    track['album']['name'],
    track.get('duration_ms'),
    track.get('popularity')
))
    conn.commit()
    conn.close()

def setup_artists_table():
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()
    
    cursor.execute('''CREATE TABLE IF NOT EXISTS artists(
        id TEXT PRIMARY KEY,
        name TEXT,
        genres TEXT,
        popularity INTEGER,
        followers INTEGER
    )
    ''')
    conn.commit()
    conn.close()

def save_artists(results):
    conn = sqlite3.connect("music.db")
    cursor = conn.cursor()
    
    for artist in results['items']:
        cursor.execute('''
    INSERT OR IGNORE INTO artists (id, name, genres, popularity, followers)
    VALUES (?, ?, ?, ?, ?)
''', (
    artist.get('id'),
    artist.get('name'),
    ', '.join(artist.get('genres', [])),
    artist.get('popularity'),
artist.get('followers', {}).get('total', 0)
))
    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    setup_database()
    print("Database Setup Complete!")
    
    