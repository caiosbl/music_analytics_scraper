import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyApiClient:
    def __init__(self, config):
        spotify_client_id = config['secrets']['spotify.api.client.id']
        spotify_client_secret = config['secrets']['spotify.api.client.secret']

        self.chunk_size = config['settings'].getint('spotify.chunk.size')
        self.api_client = spotipy.Spotify(
            auth_manager=SpotifyClientCredentials(
            client_id=spotify_client_id,
            client_secret=spotify_client_secret)
        )