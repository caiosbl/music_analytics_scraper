class SpotifyService:
    def __init__(self, config, api_client, repositories):
        self.api_client = api_client
        self.chunk_size = config['settings'].getint('spotify.chunk.size')
        self.artist_albums_repository = repositories.spotify_albums
        self.album_tracks_repository = repositories.spotify_album_tracks
        self.track_repository = repositories.spotify_track
        self.streams_repository = repositories.spotify_streams


    def fetch_artist_albums(self, spotify_artist_id):
        self.artist_albums_repository.insert_artist_albums(
            spotify_artist_id
        )


    def fetch_albums_tracks(self, spotify_artist_id):
        self.album_tracks_repository.insert_artist_album_tracks(
            spotify_artist_id
        )


    def fetch_tracks(self, spotify_artist_id):
        self.track_repository.insert_tracks(
            spotify_artist_id
        )

    def fetch_streams_count(self, spotify_artist_id):
        self.streams_repository.insert_tracks_stream_counts(
            spotify_artist_id
        )
    
    
    def run_scrap(self, spotify_artist_id):
        self.fetch_artist_albums(spotify_artist_id)
        self.fetch_albums_tracks(spotify_artist_id)
        self.fetch_tracks(spotify_artist_id)
        self.fetch_streams_count(spotify_artist_id)

    
    def update_stats(self, spotify_artist_id):
        self.run_scrap(spotify_artist_id)
    