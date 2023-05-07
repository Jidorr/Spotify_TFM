import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from spotipy_random import get_random
import time
import pandas as pd
import csv
import sqlite3

start_time = time.time()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id=cred.client_id, 
                    client_secret= cred.client_secret, 
                    redirect_uri=cred.redirect_url))

with open('../../data/df1.csv', encoding='utf8') as csv_file:
    conn = sqlite3.connect('../../data/song_database1.db')
    cursor = conn.cursor()
    conn.execute('''DROP TABLE IF EXISTS songs''')
    conn.execute('''CREATE TABLE songs
                (song_number INTEGER PRIMARY KEY AUTOINCREMENT,
                 title TEXT NOT NULL,
                 artist TEXT NOT NULL,
                 spotifyID text NOT NULL,
                 acousticness FLOAT,
                 danceability FLOAT,
                 duration_ms INTEGER,
                 energy FLOAT,
                 instrumentalness FLOAT,
                 key INTEGER,
                 liveness FLOAT,
                 loudness FLOAT,
                 mode INTEGER,
                 speechiness FLOAT,
                 tempo FLOAT,
                 time_signature INTEGER,
                 valence FLOAT);''')
    query = '''INSERT INTO songs (title, artist, spotifyID, acousticness,
                 danceability, duration_ms, energy, instrumentalness, key,
                 liveness, loudness, mode, speechiness, tempo, time_signature, valence) 
                 VALUES (?, ?, ?, ?, ?, ?,?, ?, ?,?, ?, ?,?, ?, ?, ?)'''
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    # skip the header row
    next(csv_reader)
    count = 0
    # loop through the rows and extract the song titles and artist names
    for row in csv_reader:
        try:
            song_title = row[1].lower()
            artist_name = row[3].lower()
            
            # use the song title and artist name in your query
            # for example:
            q = f'{song_title} {artist_name}'
        
            result = sp.search(q=q, type='track')
            song_id = result['tracks']['items'][0]['id']
            song_features = sp.audio_features(song_id)[0]
            cursor.execute(query, (f"{song_title}", f"{artist_name}", f"{song_id}", song_features['acousticness'],
                    song_features['danceability'], song_features['duration_ms'], song_features['energy'], 
                    song_features['instrumentalness'], song_features['key'],
                    song_features['liveness'], song_features['loudness'], song_features['mode'], 
                    song_features['speechiness'], song_features['tempo'], song_features['time_signature'], 
                    song_features['valence']))
        except:
            continue
        if (count % 5 == 0):
            time.sleep(5)
        count += 1
    # commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()