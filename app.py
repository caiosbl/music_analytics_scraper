from api_clients import SpotifyApiClient, YoutubeApiClient
from database import DatabaseManager
from services import (
    SpotifyService,
    YouTubeService,
    ArtistService,
    StatsService,
    ReportService
)
from repositories import (
    ArtistRepository,
    SpotifyAlbumsRepository,
    SpotifyAlbumTracksRepository,
    SpotifyStreamsRepository,
    SpotifyTrackRepository,
    YoutubeTrackRepository
)
from utils import setup_env
from cli import CLI

class App:
    def __init__(self):
        self.config = setup_env.init_config_with_envs("config.ini")
        self.db = DatabaseManager(self.config)
        self.db.init_db()
        self.spotify_api_client = SpotifyApiClient(self.config).api_client
        self.youtube_api_client = YoutubeApiClient(self.config).api_client
        self._init_repositories()
        self._init_services()
        self.cli = CLI(
            services=self.services,
            repositories=self.repositories,
        )


    def _init_repositories(self):
        class Repositories:
            pass

        self.repositories = Repositories()

        self.repositories.artist = ArtistRepository(
            session=self.db.session
        )

        self.repositories.spotify_albums = SpotifyAlbumsRepository(
            api_client=self.spotify_api_client,
            session=self.db.session,
            config=self.config,
        )
        self.repositories.spotify_album_tracks = SpotifyAlbumTracksRepository(
            api_client=self.spotify_api_client,
            session=self.db.session,
            config=self.config,
        )
        self.repositories.spotify_track = SpotifyTrackRepository(
            api_client=self.spotify_api_client,
            session=self.db.session,
            config=self.config,
        )
        self.repositories.spotify_streams = SpotifyStreamsRepository(
            api_client=self.spotify_api_client,
            session=self.db.session,
            config=self.config,
        )
        self.repositories.youtube_track = YoutubeTrackRepository(
            api_client=self.youtube_api_client,
            session=self.db.session,
            config=self.config,
        )

    def _init_services(self):
        class Services:
            pass

        self.services = Services()

        self.services.spotify_service = SpotifyService(
            api_client=self.spotify_api_client,
            config=self.config,
            repositories=self.repositories
        )
        self.services.youtube_service = YouTubeService(
            api_client=self.youtube_api_client,
            config=self.config,
            repositories=self.repositories
        )

        self.services.artist_service = ArtistService(
            repositories=self.repositories,
            session=self.db.session
        )

        self.services.stats_service = StatsService(
            session=self.db.session,
            repositories=self.repositories,
            services=self.services
        )

        self.services.report_service = ReportService(
            repositories=self.repositories
        )

    def run(self):
        self.cli.cli()


if __name__ == "__main__":
    App().run()

