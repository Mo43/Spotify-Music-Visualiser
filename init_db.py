import sqlite3

conn = sqlite3.connect("music.db")
schema = open("schema.sql").read()

conn.executescript(schema)
conn.close()
