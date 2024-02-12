import click
import tqdm
from rich.console import Console
from rich.table import Table
from services.artist_service import ArtistNotFoundError

console = Console()

class CLI:
    def __init__(
            self,
            services,
            repositories,
        ):
        self.artist_repository = repositories.artist
        self.artist_service = services.artist_service
        self.spotify_service = services.spotify_service
        self.youtube_service = services.youtube_service
        self.stats_service = services.stats_service
        self.setup_cli_commands()

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
            console.print(f"Artist {name} added successfully", style="green")

        @cli.command()
        @click.option('--artist_id', prompt='Artist ID', help='Artist ID', required=True)
        @click.option('--name', prompt='Artist name', help='Artist name', required=False, default="")
        @click.option('--spotify_id', prompt='Spotify ID', help='Artist Spotify ID', required=False, default="")
        @click.option('--youtube_id', prompt='YouTube ID', help='Artist YouTube Channel ID', required=False, default="")
        @click.option('--deezer_id', prompt='Deezer ID', help='Artist Deezer ID', required=False, default="")
        @click.option('--apple_music_id', prompt='Apple Music ID', help='Artist Apple Music ID', required=False, default="")
        @click.option('--amazon_music_id', prompt='Amazon Music ID', help='Artist Amazon Music ID', required=False, default="")
        @click.option('--tidal_id', prompt='Tidal ID', help='Artist Tidal ID', required=False, default="")
        def update_artist(
            artist_id,
            name,
            spotify_id,
            youtube_id,
            deezer_id,
            apple_music_id,
            amazon_music_id,
            tidal_id
        ):
            try:
                artist = self.artist_service.update_artist(
                    artist_id,
                    name,
                    spotify_id,
                    youtube_id,
                    deezer_id,
                    apple_music_id,
                    amazon_music_id,
                    tidal_id
                )
                console.print(f"Artist {artist.name} updated successfully", style="green")
            except ArtistNotFoundError as e:
                console.print_exception(e)

        @cli.command()
        @click.option('--artist_id', prompt='Artist ID', help='Artist ID', required=True)
        @click.option('--skip_spotify', is_flag=True, help='Skip Spotify')
        @click.option('--skip_youtube', is_flag=True, help='Skip YouTube')
        def update_artist_stats(artist_id, skip_spotify, skip_youtube):
            artist = self.artist_repository.get_artist(artist_id)
            console.print(f"Updating stats for artist {artist.name}", style="green")

            if not artist:
                console.print_exception(ArtistNotFoundError(f"Artist with id {artist_id} not found"))
                return
            
            self.stats_service.update_artist_stats(artist, skip_spotify, skip_youtube)

        @cli.command()
        @click.option('--skip_spotify', is_flag=True, help='Skip Spotify')
        @click.option('--skip_youtube', is_flag=True, help='Skip YouTube')
        @click.option('--only_without_stats', is_flag=True, help='Update only artists without stats')
        def update_all_artists_stats(skip_spotify, skip_youtube, only_without_stats):
            artists = self.artist_repository.get_all_artists() \
                if not only_without_stats else self.artist_repository.get_artists_without_stats()
            with tqdm.tqdm(total=len(artists), desc="Updating artists stats") as pbar:
                for artist in artists:
                    console.print(f"Updating stats for artist {artist.name}", style="green")
                    self.stats_service.update_artist_stats(artist, skip_spotify, skip_youtube)
                    pbar.update(1)


        @cli.command()
        def list_artists():
            table = Table(title="Artists")
            table.add_column("Name", style="cyan")
            table.add_column("ID", style="green")
            table.add_column("Last stats update", style="blue")
            table.add_column("Spotify ID", style="magenta")
            table.add_column("YouTube ID", style="yellow")
            table.add_column("Deezer ID", style="red")
            table.add_column("Apple Music ID", style="blue")
            table.add_column("Amazon Music ID", style="green")
            table.add_column("Tidal ID", style="magenta")

            artists = self.artist_repository.get_all_artists()
            for artist in artists:
                table.add_row(
                    artist.name,
                    str(artist.id),
                    str(artist.last_stats_update),
                    artist.spotify_id,
                    artist.youtube_id,
                    artist.deezer_id,
                    artist.apple_music_id,
                    artist.amazon_music_id,
                    artist.tidal_id
                )
            
            console.print(table)

        self.cli = cli
