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

with open('../../data/files/song_data.csv', encoding='utf8') as csv_file:
    conn = sqlite3.connect('../../data/database/song_database2.db')
    cursor = conn.cursor()
    conn.execute('''DROP TABLE IF EXISTS songs''')
    conn.execute('''CREATE TABLE songs
                (id INTEGER PRIMARY KEY,name TEXT NOT NULL,album TEXT NOT NULL,album_id TEXT NOT NULL,
                 artists TEXT NOT NULL,artists_ids TEXT NOT NULL,track_number INTEGER,disc_number INTEGER,
                 explicit INTEGER,danceability FLOAT,energy FLOAT,key INTEGER,loudness FLOAT,mode INTEGER,
                 speechiness FLOAT,acousticness FLOAT,instrumentalness FLOAT,liveness FLOAT,duration_ms INTEGER,
                 valence FLOAT,tempo FLOAT,duration_ms INTEGER,time_signature INTEGER,year INTEGER,release_date DATE
                 );''')
    query = '''INSERT INTO songs (id, name, album, album_id, 
    artists, artist_ids, track_number, disc_number, explicit, 
    danceability, energy, key, loudness, mode, speechiness, acousticness, 
    instrumentalness, liveness, valence, tempo, duration_ms, time_signature, 
    year, release_date) 
                 VALUES (?, ?, ?, ?, ?, ?,?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?,?, ?, ?)'''
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
            cursor.execute(query, (f"{song_id}", f"{song_title}", song_features['album'], 
                                   song_features['album_id'], song_features['artists'], 
                                   song_features['artist_ids'], song_features['track_number'], 
                                   song_features['disc_number'], song_features['explicit'], 
                                   song_features['danceability'], song_features['energy'], 
                                   song_features['key'], song_features['loudness'], 
                                   song_features['mode'], song_features['speechiness'], 
                                   song_features['acousticness'], song_features['instrumentalness'], 
                                   song_features['liveness'], song_features['valence'], 
                                   song_features['tempo'], song_features['duration_ms'], 
                                   song_features['time_signature'], song_features['year'], 
                                   song_features['release_date']
))
        except:
            continue
        if (count % 5 == 0):
            time.sleep(5)
        count += 1
    # commit the changes and close the connection
    conn.commit()
    cursor.close()
    conn.close()