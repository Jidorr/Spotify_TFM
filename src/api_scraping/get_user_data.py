import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
from spotipy_random import get_random
import time
import pandas as pd
import csv
import sqlite3
from user_functions import *

start_time = time.time()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id=cred.client_id, 
                    client_secret= cred.client_secret, 
                    redirect_uri=cred.redirect_url))

conn = sqlite3.connect('../../data/database/song_database.db')
cursor = conn.cursor()

query = '''INSERT INTO songs (id, name, album, album_id, 
    artists, artist_ids, track_number, disc_number, explicit, 
    danceability, energy, key, loudness, mode, speechiness, acousticness, 
    instrumentalness, liveness, valence, tempo, duration_ms, time_signature, 
    year, release_date) 
                 VALUES (?, ?, ?, ?, ?, ?,?, ?, ?,?, ?, ?, ?, ?, ?, ?, ?, ?,?, ?, ?,?, ?, ?)'''

all_playlists = getUserPlaylists()

for playlist_id in all_playlists.values():
    songs = getSongsInPlaylist(playlist_id)
    for i, song in enumerate(songs.values()):
        try:
            info = sp.track(song)
            album, album_id, artists, artists_ids, track_number, disc_number, explicit, release_date = info['album']['name'], info['album']['id'], info['album']['artists'][0]['name'], info['album']['artists'][0]['id'], info['track_number'],info['disc_number'], info['explicit'], info['album']['release_date']
            song_info = getSongInformation(song)[0]
            cursor.execute(query, (song_info['id'], list(songs.keys())[i], album, 
                        album_id, artists, artists_ids, track_number, disc_number, explicit, 
                        song_info['danceability'], song_info['energy'], 
                        song_info['key'], song_info['loudness'], 
                        song_info['mode'], song_info['speechiness'], 
                        song_info['acousticness'], song_info['instrumentalness'], 
                        song_info['liveness'], song_info['valence'], 
                        song_info['tempo'], song_info['duration_ms'], 
                        song_info['time_signature'], release_date[:4], 
                        release_date))
            print(f'inserted song {list(songs.keys())[i]}')
        except:
            print('exception')
            continue
    print(f'completed playlist {playlist_id}')
conn.commit()
cursor.close()
conn.close()

