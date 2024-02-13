import datetime
from rich.console import Console

console = Console()

class StatsService:
    def __init__(self, session, repositories, services):
        self.session = session
        self.artist_repository = repositories.artist
        self.spotify_service = services.spotify_service
        self.youtube_service = services.youtube_service
    
    def update_artist_stats(self, artist, skip_spotify, skip_youtube):
        if not skip_youtube:
            console.print(f"Updating YouTube stats for artist {artist.name}", style="green")
            self.youtube_service.update_stats(artist.youtube_id)

        if not skip_spotify:
            console.print(f"Updating Spotify stats for artist {artist.name}", style="green")
            self.spotify_service.update_stats(artist.spotify_id)

        artist.last_stats_update = datetime.datetime.utcnow()
        self.session.commit()
