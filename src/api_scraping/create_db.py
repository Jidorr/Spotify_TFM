import pandas as pd
import sqlite3

# Read the CSV file into a pandas dataframe
df = pd.read_csv("../../data/files/tracks_features.csv")

# Connect to a SQLite database
conn = sqlite3.connect('../../data/database/song_database.db')

# Create a new table in the database (if it doesn't exist)
df.to_sql('songs', conn, if_exists='replace', index=False)

# Commit the changes and close the connection
conn.commit()
conn.close()