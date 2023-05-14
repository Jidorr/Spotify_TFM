import spotipy
from spotipy.oauth2 import SpotifyOAuth
import cred
import time

start_time = time.time()
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
                    client_id=cred.client_id, 
                    client_secret= cred.client_secret, 
                    redirect_uri=cred.redirect_url))

def getUserRecentTracks():
    tracks = {}
    for item in (sp.current_user_recently_played(limit=10)['items']):
        tracks[item['track']['name']] = item['track']['id']
    return tracks

def getUserPlaylists():
    ids = {}
    for item in (sp.current_user_playlists()['items']):
        ids[item['name']] = item['id']
    return ids

def getSongsInPlaylist(playlist_id):
    tracks = {}
    for item in (sp.playlist_tracks(playlist_id)['items']):
        tracks[item['track']['name']] = item['track']['id']
    return tracks

def getSongInformation(song_id):
    song_features = sp.audio_features(song_id)
    return song_features
