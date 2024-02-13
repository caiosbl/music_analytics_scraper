from rich.console import Console
from rich.table import Table
from models.artist_report import ArtistReport
from services.artist_service import ArtistNotFoundError
from utils.format import format_number

console = Console()

class ReportService:
    def __init__(self, repositories):
        self.repositories = repositories
        self.artist_repository = repositories.artist


    def get_artist_report(self, artist_id):
        artist = self.artist_repository.get_artist(artist_id)

        if not artist:
            raise ArtistNotFoundError(f"Artist with id {artist_id} not found")

        return ArtistReport(artist, self.repositories)
    
    def show_youtube_artist_report(self, artist_id):
        artist_report = self.get_artist_report(artist_id)
        artist_report.print_youtube_report()

    def show_spotify_artist_report(self, artist_id):
        artist_report = self.get_artist_report(artist_id)
        artist_report.print_spotify_report()

    def _compare_absolute_metric(self, metric, value_1, value_2, artist_1, artist_2):
        return (
            metric,
            format_number(value_1),
            format_number(value_2),
            artist_1 if value_1 > value_2 else artist_2
        )
    
    def _compare_relative_metric(self, metric, value_1, value_2, title_1, title_2, artist_1, artist_2):
        return (
            metric,
            f"{format_number(value_1)} ({title_1})",
            f"{format_number(value_2)} ({title_2})",
            artist_1 if value_1 > value_2 else artist_2
        )
        

    def compare_artist_reports(self, artist_id_1, artist_id_2):
        artist1 = self.artist_repository.get_artist(artist_id_1)
        artist2 = self.artist_repository.get_artist(artist_id_2)

        if not artist1:
            raise ArtistNotFoundError(f"Artist with id {artist_id_1} not found")
        elif not artist2:
            raise ArtistNotFoundError(f"Artist with id {artist_id_2} not found")
        
        artist_report_1 = self.get_artist_report(artist_id_1)
        artist_report_2 = self.get_artist_report(artist_id_2)

        artist_1 = artist_report_1.artist
        artist_2 = artist_report_2.artist

        artist_1_top_10_spotify_track = artist_report_1.top_10_spotify_tracks()
        artist_2_top_10_spotify_track = artist_report_2.top_10_spotify_tracks()
        artist_1_top_10_youtube_track = artist_report_1.top_10_youtube_tracks()
        artist_2_top_10_youtube_track = artist_report_2.top_10_youtube_tracks()

        compare_table = Table(title=f"{artist_1.name} vs {artist_2.name}")

        compare_table.add_column("Metric", style="bold blue")
        compare_table.add_column(artist_1.name, style="bold blue")
        compare_table.add_column(artist_2.name, style="bold blue")
        compare_table.add_column("Winner", style="bold blue")


        
        compare_table.add_row(
            *self._compare_absolute_metric(
                "Total Spotify Streams",
                artist_report_1.total_of_spotify_streams(),
                artist_report_2.total_of_spotify_streams(),
                artist_1.name,
                artist_2.name
            )
        )

        compare_table.add_row(
            *self._compare_absolute_metric(
                "Total Youtube Views",
                artist_report_1.total_of_youtube_views(),
                artist_report_2.total_of_youtube_views(),
                artist_1.name,
                artist_2.name
            )
        )

        compare_table.add_row(
            *self._compare_absolute_metric(
                "Total Youtube Likes",
                artist_report_1.total_of_youtube_likes(),
                artist_report_2.total_of_youtube_likes(),
                artist_1.name,
                artist_2.name
            )
        )

        compare_table.add_row(
            *self._compare_relative_metric(
                "Most Popular Spotify Track Streams",
                artist_1_top_10_spotify_track[0].streams,
                artist_2_top_10_spotify_track[0].streams,
                artist_1_top_10_spotify_track[0].name,
                artist_2_top_10_spotify_track[0].name,
                artist_1.name,
                artist_2.name
            )
        )

        compare_table.add_row(
            *self._compare_relative_metric(
                "Most Popular Youtube Track Views",
                artist_1_top_10_youtube_track[0].views,
                artist_2_top_10_youtube_track[0].views,
                artist_1_top_10_youtube_track[0].name,
                artist_2_top_10_youtube_track[0].name,
                artist_1.name,
                artist_2.name
            )
        )

        compare_table.add_row(
            *self._compare_relative_metric(
                "Most Popular Youtube Track Likes",
                artist_1_top_10_youtube_track[0].like_count,
                artist_2_top_10_youtube_track[0].like_count,
                artist_1_top_10_youtube_track[0].name,
                artist_2_top_10_youtube_track[0].name,
                artist_1.name,
                artist_2.name
            )
        )

        console.print(compare_table)
