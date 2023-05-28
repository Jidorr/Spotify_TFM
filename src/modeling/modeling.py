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

conn = sqlite3.connect("../../data/database/song_database.db")
dataset = pd.read_sql_query("SELECT * FROM songs2", conn)

# Select the features for clustering
all_features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo',
            'duration_ms', 'time_signature']

features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness',
            'acousticness', 'instrumentalness', 'valence', 'tempo',
            'time_signature']

scaler = StandardScaler()
dataset[features] = scaler.fit_transform(dataset[features])

# Fit the k-means model
k = 5  # Specify the number of clusters
kmeans = KMeans(n_clusters=k, random_state=42, n_init='auto')
kmeans.fit(dataset[features])

with open("../../data/model/model.pkl", "wb") as f:
    pickle.dump(kmeans, f)

# Choose a song to find similar songs
chosen_song = dataset[dataset['id'] == '0htMxjQHDMnrt8as3Z3uFo']  # Replace with your chosen song

# Get the cluster label for the chosen song
chosen_song_cluster = kmeans.predict(chosen_song[features])[0]

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

# Display the closest songs
closest_songs = result_df.head(10)  # Adjust the number of closest songs as desired
print(closest_songs)
