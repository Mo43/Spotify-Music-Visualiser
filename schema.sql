CREATE TABLE IF NOT EXISTS artists (
    id  TEXT PRIMARY KEY,
    name    TEXT NOT NULL,
    image_url   TEXT,
    spotify_url TEXT
);

CREATE TABLE IF NOT EXISTS albums (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    album_type  TEXT,
    release_date    TEXT,
    release_year    INTEGER,            
    total_tracks    INTEGER,
    image_url   TEXT,
    spotify_url TEXT
);

CREATE TABLE IF NOT EXISTS tracks (
    id  TEXT PRIMARY KEY,
    name    TEXT NOT NULL,
    album_id    TEXT NOT NULL,    
    duration_ms INTEGER,
    explicit    INTEGER,
    track_number    INTEGER,
    isrc    TEXT,
    spotify_url TEXT,
    FOREIGN KEY (album_id) REFERENCES albums(id)
);

CREATE TABLE IF NOT EXISTS track_artists (
    track_id  TEXT NOT NULL,
    artist_id TEXT NOT NULL,
    position  INTEGER,
    PRIMARY KEY (track_id, artist_id),
    FOREIGN KEY (track_id) REFERENCES tracks(id),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

CREATE TABLE IF NOT EXISTS plays (
    id           INTEGER PRIMARY KEY AUTOINCREMENT,
    track_id     TEXT NOT NULL,
    played_at    TEXT NOT NULL,
    context_type TEXT,
    context_uri  TEXT,
    UNIQUE (track_id, played_at),
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);

