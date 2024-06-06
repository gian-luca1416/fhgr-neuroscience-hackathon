import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config


class SpotifyClient:
    def __init__(self):
        self.scope = "user-library-read, user-read-currently-playing, playlist-read-private, playlist-modify-private, playlist-modify-public"
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(scope=self.scope, client_id=config.client_id, client_secret=config.client_secret,
                                      redirect_uri="http://localhost:8080"))

    def trigger(self):
        current_track = self.sp.current_user_playing_track()
        playlists = self.sp.current_user_playlists(offset=0)

        fhgr_playlist = None

        for playlist in playlists["items"]:
            if playlist["name"] == "personal_favs":
                fhgr_playlist = playlist
                break

        if current_track != None:
            self.sp.playlist_add_items(fhgr_playlist["id"], [current_track["item"]["id"]])
