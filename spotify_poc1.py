import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-library-read, user-read-currently-playing, playlist-read-private, playlist-modify-private, playlist-modify-public"
client_id = ""
client_secret = ""

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://localhost:8080"))

current_track = sp.current_user_playing_track()
playlists = sp.current_user_playlists(offset=0)

fhgr_playlist = None

for playlist in playlists['items']:
    if playlist['name'] == 'fhgr':
        fhgr_playlist = playlist
        break

if current_track != None:
    sp.playlist_add_items(fhgr_playlist['id'], [current_track['item']['id']])

