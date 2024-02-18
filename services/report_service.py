import openpyxl
from rich.console import Console
from rich.table import Table
from models.artist_report import ArtistReport
from services.artist_service import ArtistNotFoundError
from utils.format import format_number
import os

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
            "N/A",
            format_number(value_2),
            "N/A",
            artist_1 if value_1 > value_2 else artist_2,
        )

    def _compare_relative_metric(
        self, metric, value_1, value_2, title_1, title_2, artist_1, artist_2
    ):
        return (
            metric,
            format_number(value_1),
            title_1,
            format_number(value_2),
            title_2,
            artist_1 if value_1 > value_2 else artist_2,
        )
    
    def save_comparison_to_file(
        self, artist_1, artist_2, rows
    ):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = f"{artist_1.name} vs {artist_2.name}"

        ws.append([
            "Metric",
            f"{artist_1.name} - Metric value",
            f"{artist_1.name} - Track name",
            f"{artist_2.name} - Metric value",
            f"{artist_2.name} - Track name", "Winner"
        ])

        for row in rows:
            ws.append([cell for cell in row])

        file_path = f"reports/{artist_1.name.replace(" ", "_")}_vs_{artist_2.name.replace(" ", "_")}.xlsx"
        os.makedirs("reports", exist_ok=True)
        wb.save(file_path)

    def compare_artist_reports(self, artist_id_1, artist_id_2, save_to_file=False):
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

        class FileTable:
            pass

        compare_table = Table(title=f"{artist_1.name} vs {artist_2.name}")

        compare_table.add_column("Metric", style="bold blue")
        compare_table.add_column(f"{artist_1.name} - Metric value", style="bold blue")
        compare_table.add_column(f"{artist_1.name} - Track name", style="bold blue")
        compare_table.add_column(f"{artist_2.name} - Metric value", style="bold blue")
        compare_table.add_column(f"{artist_2.name} - Track name", style="bold blue")
        compare_table.add_column("Winner", style="bold blue")

        row1 = self._compare_absolute_metric(
                "Total Spotify Streams",
                artist_report_1.total_of_spotify_streams(),
                artist_report_2.total_of_spotify_streams(),
                artist_1.name,
                artist_2.name,
            )
        
        row2 = self._compare_absolute_metric(
                "Total Youtube Views",
                artist_report_1.total_of_youtube_views(),
                artist_report_2.total_of_youtube_views(),
                artist_1.name,
                artist_2.name,
            )
        
        row3 = self._compare_absolute_metric(
                "Total Youtube Likes",
                artist_report_1.total_of_youtube_likes(),
                artist_report_2.total_of_youtube_likes(),
                artist_1.name,
                artist_2.name,
            )
        
        row4 = self._compare_relative_metric(
                "Most Popular Spotify Track Streams",
                artist_1_top_10_spotify_track[0].streams,
                artist_2_top_10_spotify_track[0].streams,
                artist_1_top_10_spotify_track[0].name,
                artist_2_top_10_spotify_track[0].name,
                artist_1.name,
                artist_2.name,
            )
        
        row5 = self._compare_relative_metric(
                "Most Popular Youtube Track Views",
                artist_1_top_10_youtube_track[0].views,
                artist_2_top_10_youtube_track[0].views,
                artist_1_top_10_youtube_track[0].name,
                artist_2_top_10_youtube_track[0].name,
                artist_1.name,
                artist_2.name,
            )
        
        row6 = self._compare_relative_metric(
                "Most Popular Youtube Track Likes",
                artist_1_top_10_youtube_track[0].like_count,
                artist_2_top_10_youtube_track[0].like_count,
                artist_1_top_10_youtube_track[0].name,
                artist_2_top_10_youtube_track[0].name,
                artist_1.name,
                artist_2.name,
            )
        
        row7 = self._compare_absolute_metric(
                "Average Spotify Track Streams",
                artist_report_1.average_of_spotify_streams(),
                artist_report_2.average_of_spotify_streams(),
                artist_1.name,
                artist_2.name,
            )
        
        row8 = self._compare_absolute_metric(
                "Average Youtube Track Views",
                artist_report_1.average_of_youtube_views(),
                artist_report_2.average_of_youtube_views(),
                artist_1.name,
                artist_2.name,
            )
        
        row9 = self._compare_absolute_metric(
                "Total Spotify Tracks",
                artist_report_1.total_of_spotify_tracks(),
                artist_report_2.total_of_spotify_tracks(),
                artist_1.name,
                artist_2.name,
            )
        
        row10 = self._compare_absolute_metric(
                "Total Youtube Tracks",
                artist_report_1.total_of_youtube_tracks(),
                artist_report_2.total_of_youtube_tracks(),
                artist_1.name,
                artist_2.name,
            )
        
        table_rows = [row1, row2, row3, row4, row5, row6, row7, row8, row9, row10]

        for row in table_rows:
            compare_table.add_row(*row)

        console.print(compare_table)

        if save_to_file:
            console.print("Saving comparison to file...", style="yellow")
            self.save_comparison_to_file(
                artist_1, artist_2, table_rows
            )
            console.print("Comparison saved to file", style="green")

