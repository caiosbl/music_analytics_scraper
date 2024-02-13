import locale
from rich.console import Console
from rich.table import Table
from utils.format import format_number

locale.setlocale(locale.LC_ALL, 'en_US')
console = Console()

class ArtistReport:
    def __init__(self, artist, repositories):
        self.artist = artist
        self.artist_repository = repositories.artist
        self.spotify_track_repository = repositories.spotify_track
        self.youtube_track_repository = repositories.youtube_track


    def total_of_spotify_streams(self):
        return self.spotify_track_repository.get_total_of_streams(
            self.artist.spotify_id
        )

    def top_10_spotify_tracks(self):
        return self.spotify_track_repository.get_top_10_tracks(
            self.artist.spotify_id
        )
    
    def total_of_youtube_views(self):
        return self.youtube_track_repository.get_total_of_views(
            self.artist.youtube_id
        )
    
    def top_10_youtube_tracks(self):
        return self.youtube_track_repository.get_top_10_tracks(
            self.artist.youtube_id
        )
    
    def total_of_youtube_likes(self):
        return self.youtube_track_repository.get_total_of_likes(
            self.artist.youtube_id
        )
    
    def print_youtube_report(self):
        youtube_top_10_table = Table(title=f"Top 10 {self.artist.name} Youtube Tracks")
        youtube_top_10_table.add_column("Name", style="bold blue")
        youtube_top_10_table.add_column("Views", style="bold blue")
        youtube_top_10_table.add_column("Likes", style="bold blue")

        for track in self.top_10_youtube_tracks():
            youtube_top_10_table.add_row(
                track.name,
                format_number(track.views),
                format_number(track.like_count),
            )

        console.print(youtube_top_10_table)

    def print_spotify_report(self):
        spotify_top_10_table = Table(title=f"Top 10 {self.artist.name} Spotify Tracks")
        spotify_top_10_table.add_column("Name", style="bold blue")
        spotify_top_10_table.add_column("Streams", style="bold blue")

        for track in self.top_10_spotify_tracks():
            spotify_top_10_table.add_row(
                track.name,
                format_number(track.streams),
            )

        console.print(spotify_top_10_table)
