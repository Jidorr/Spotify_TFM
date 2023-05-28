import os
import sys
import pandas as pd
import numpy as np 
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
import pickle
import sys

# Afegim el directori al path per importar els mòduls necessaris
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path+"\\api_scraping")
    sys.path.append(module_path+"\\functions")
from user_functions import *

import sqlite3

# Demanem a l'usuari què vol fer
inp = input('''***
Escriu 1 per generar cançons a partir de les últimes cançons escoltades.
Escriu 2 per generar cançons a partir de les teves playlists
***\n''')

if (inp == '2'):
    # Obtenim les playlists de l'usuari
    playlists = getUserPlaylists()
    print(playlists)
    inp2 = input('''***
Escriu la id de la playlist:
***\n''')
    # Obtenim les cançons de la playlist seleccionada
    tracks = list(getSongsInPlaylist(inp2).values())
else:
    # Obtenim les últimes cançons escoltades per l'usuari
    tracks = list(getUserRecentTracks().values())

# Connectem a la base de dades SQLite
conn = sqlite3.connect("../../data/database/song_database.db")

# Llegim les dades de la taula "songs2"
dataset = pd.read_sql_query("SELECT * FROM songs2", conn)

# Carreguem el model KMeans entrenat
with open("../../data/model/model.pkl", "rb") as f:
    kmeans = pickle.load(f)

# Seleccionem les característiques per a l'anàlisi
features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'valence', 'tempo',
            'time_signature']

# Normalitzem les característiques
scaler = StandardScaler()
dataset[features] = scaler.fit_transform(dataset[features])

df = []
for id in tracks:
    # Triem una cançó per trobar cançons similars
    chosen_song = dataset[dataset['id'] == id].head(1) 
    
    # Obtenim l'etiqueta del clúster per a la cançó triada
    try: 
        chosen_song_cluster = kmeans.predict(chosen_song[features])[0]
    except:
        continue

    # Filtrem el conjunt de dades per incloure només les cançons del mateix clúster
    cluster_songs = dataset[kmeans.labels_ == chosen_song_cluster]

    # Calculeem la distància fins a la cançó triada per a cada cançó del clúster
    distances = cdist(chosen_song[features], cluster_songs[features])

    # Creem un DataFrame amb les distàncies i els detalls de les cançons
    result_df = pd.DataFrame({
        'Distància': distances.flatten(),
        'Nom de la Cançó': cluster_songs['name'],
        'Artista': cluster_songs['artists'],
    })
    # Ordenem el DataFrame per distància (ascendent)
    result_df.sort_values('Distància', inplace=True)
    result_df = result_df.loc[result_df['Nom de la Cançó'] != chosen_song.name.item()].head(2)
    df.append(result_df)

# Mostre les cançons més properes
df = pd.concat(df)
print(df)
