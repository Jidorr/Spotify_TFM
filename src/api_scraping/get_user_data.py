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
    return sp.current_user_recently_played(limit=10)

def getUserPlaylists():
    return sp.current_user_playlists()

def getUserSongsInPlaylist(playlist_name):
    pass

print(getUserPlaylists())