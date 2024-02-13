from models.artist import Artist
from models.artist_report import ArtistReport
from services.artist_service import ArtistNotFoundError

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
