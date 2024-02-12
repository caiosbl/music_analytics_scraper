import click
import tqdm
from services.artist_service import ArtistNotFoundError

class CLI:
    def __init__(
            self,
            services,
            repositories
        ):
        self.artist_repository = repositories.artist
        self.artist_service = services.artist_service
        self.spotify_service = services.spotify_service
        self.youtube_service = services.youtube_service
        self.setup_cli_commands()

    def _update_artist_stats(self, artist, skip_spotify, skip_youtube):
        if not skip_youtube:
            self.youtube_service.update_stats(artist.youtube_id)

        if not skip_spotify:
            self.spotify_service.update_stats(artist.spotify_id)

    def setup_cli_commands(self):
        @click.group()
        def cli():
            pass

        @cli.command()
        @click.option('--name', prompt='Artist name', help='Artist name')
        @click.option('--spotify_id', prompt='Spotify ID', help='Artist Spotify ID', required=False, default="")
        @click.option('--youtube_id', prompt='YouTube ID', help='Artist YouTube Channel ID', required=False, default="")
        @click.option('--deezer_id', prompt='Deezer ID', help='Artist Deezer ID', required=False, default="")
        @click.option('--apple_music_id', prompt='Apple Music ID', help='Artist Apple Music ID', required=False, default="")
        @click.option('--amazon_music_id', prompt='Amazon Music ID', help='Artist Amazon Music ID', required=False, default="")
        @click.option('--tidal_id', prompt='Tidal ID', help='Artist Tidal ID', required=False, default="")
        def add_artist(
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
        @click.option('--skip_spotify', is_flag=True, help='Skip Spotify')
        @click.option('--skip_youtube', is_flag=True, help='Skip YouTube')
        def update_artist_stats(artist_id, skip_spotify, skip_youtube):
            artist = self.artist_repository.get_artist(artist_id)
            if not artist:
                print(f"Artist {artist_id} not found")
                return
            
            self._update_artist_stats(artist, skip_spotify, skip_youtube)

        @cli.command()
        @click.option('--skip_spotify', is_flag=True, help='Skip Spotify')
        @click.option('--skip_youtube', is_flag=True, help='Skip YouTube')
        def update_all_artists_stats(skip_spotify, skip_youtube):
            artists = self.artist_service.get_all_artists()
            with tqdm.tqdm(total=len(artists), desc="Updating artists stats") as pbar:
                for artist in artists:
                    print(f"Updating stats for artist {artist.name}")
                    self._update_artist_stats(artist, skip_spotify, skip_youtube)
                    pbar.update(1)

        self.cli = cli
