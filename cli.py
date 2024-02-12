import click
from services.artist_service import ArtistNotFoundError

class CLI:
    def __init__(
            self,
            config,
            services
        ):
        self.config = config
        self.artist_service = services.artist_service
        self.spotify_service = services.spotify_service
        self.youtube_service = services.youtube_service

    @click.group()
    def cli(self):
        pass

    @cli.command()
    @click.option('--name', prompt='Artist name', help='Artist name')
    @click.option('--spotify_id', prompt='Spotify ID', help='Artist Spotify ID')
    @click.option('--youtube_id', prompt='YouTube ID', help='Artist YouTube Channel ID')
    @click.option('--deezer_id', prompt='Deezer ID', help='Artist Deezer ID')
    @click.option('--apple_music_id', prompt='Apple Music ID', help='Artist Apple Music ID')
    @click.option('--amazon_music_id', prompt='Amazon Music ID', help='Artist Amazon Music ID')
    @click.option('--tidal_id', prompt='Tidal ID', help='Artist Tidal ID')
    def add_artist(
        self,
        name,
        spotify_id,
        youtube_id,
        deezer_id,
        apple_music_id,
        amazon_music_id,
        tidal_id
    ):
        self.artist_service.insert_artist(
            name,
            spotify_id,
            youtube_id,
            deezer_id,
            apple_music_id,
            amazon_music_id,
            tidal_id
        )
        print(f"Artist {name} added successfully")

    @cli.command()
    @click.argument('artist_id', required=True)
    @click.option('--spotify_id', prompt='Spotify ID', help='Artist Spotify ID')
    @click.option('--youtube_id', prompt='YouTube ID', help='Artist YouTube Channel ID')
    @click.option('--deezer_id', prompt='Deezer ID', help='Artist Deezer ID')
    @click.option('--apple_music_id', prompt='Apple Music ID', help='Artist Apple Music ID')
    @click.option('--amazon_music_id', prompt='Amazon Music ID', help='Artist Amazon Music ID')
    @click.option('--tidal_id', prompt='Tidal ID', help='Artist Tidal ID')
    def update_artist(
        self,
        artist_id,
        spotify_id,
        youtube_id,
        deezer_id,
        apple_music_id,
        amazon_music_id,
        tidal_id
    ):
        try:
            self.artist_service.update_artist(
                artist_id,
                spotify_id,
                youtube_id,
                deezer_id,
                apple_music_id,
                amazon_music_id,
                tidal_id
            )
            print(f"Artist {artist_id} updated successfully")
        except ArtistNotFoundError as e:
            print(f"Error: {e}")


    @cli.command()
    @click.argument('artist_id', required=True)
    def update_artist_stats(self):
        pass

    
    def run(self):
        print(f"Running with config: {self.config}")
