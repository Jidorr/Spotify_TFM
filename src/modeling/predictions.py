import sys
import os
import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
import pickle
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path+"\\api_scraping")
    sys.path.append(module_path+"\\functions")
from user_functions import *
import sqlite3


inp = input('''***
Escriu 1 per generar cançons a partir de les últimes cançons escoltades.
Escriu 2 per generar cançons a partir de les teves playlists
***\n''')

if (inp == '2'):
    playlists = getUserPlaylists()
    print(playlists)
    inp2 = input('''***
Escriu la id de la playlist:
***\n''')
    tracks = list(getSongsInPlaylist(inp2).values())
else:
    tracks = list(getUserRecentTracks().values())

conn = sqlite3.connect("../../data/database/song_database.db")
dataset = pd.read_sql_query("SELECT * FROM songs2", conn)

with open("../../data/model/model.pkl", "rb") as f:
    kmeans = pickle.load(f)

features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'valence', 'tempo',
            'time_signature']

scaler = StandardScaler()
dataset[features] = scaler.fit_transform(dataset[features])

df = []
for id in tracks:
    # Choose a song to find similar songs
    chosen_song = dataset[dataset['id'] == id].head(1)  # Replace with your chosen song
    
    # Get the cluster label for the chosen song
    try: 
        chosen_song_cluster = kmeans.predict(chosen_song[features])[0]
    except:
        continue

    # Filter the dataset to include only the songs in the same cluster
    cluster_songs = dataset[kmeans.labels_ == chosen_song_cluster]

    # Calculate the distance to the chosen song for each song in the cluster
    distances = cdist(chosen_song[features], cluster_songs[features])

    # Create a DataFrame with distances and song details
    result_df = pd.DataFrame({
        'Distance': distances.flatten(),
        'Song Name': cluster_songs['name'],
        'Artist': cluster_songs['artists'],
        # Add more columns as per your requirement
    })
    
    # Sort the DataFrame by distance (ascending)
    result_df.sort_values('Distance', inplace=True)
    result_df = result_df.loc[result_df['Song Name'] != chosen_song.name.item()].head(2)
    # Display the closest songs
    df.append(result_df)

df = pd.concat(df)
print(df)