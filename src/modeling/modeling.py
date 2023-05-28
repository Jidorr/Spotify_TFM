# Importem els mòduls necessaris
import sys
import os
import pandas as pd
from sklearn.cluster import KMeans
from scipy.spatial.distance import cdist
from sklearn.preprocessing import StandardScaler
import pickle
import sqlite3
# Afegim el directori al path per importar els mòduls necessaris
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path+"\\api_scraping")
    sys.path.append(module_path+"\\functions")
from user_functions import *

# Connectem a la base de dades SQLite
conn = sqlite3.connect("../../data/database/song_database.db")

# Llegim les dades de la taula "songs2"
dataset = pd.read_sql_query("SELECT * FROM songs2", conn)

# Seleccionem les característiques per a l'agrupació
all_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'duration_ms', 'time_signature']

features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'valence', 'tempo',
            'time_signature']

# Normalitzem les característiques
scaler = StandardScaler()
dataset[features] = scaler.fit_transform(dataset[features])

# Entrenem el model KMeans
k = 5  # Especifica el nombre de clústers
kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
kmeans.fit(dataset[features])

# Guardem el model en un fitxer
with open("../../data/model/model.pkl", "wb") as f:
    pickle.dump(kmeans, f)