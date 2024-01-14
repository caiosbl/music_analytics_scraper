import argparse
import configparser

from api_clients import SpotifyApiClient, YoutubeApiClient
from database import DatabaseManager
from scrapers.spotify_scrap import SpotifyScrap
from scrapers.youtube_scrap import YouTubeScraper
from repositories import SpotifyAlbumsRepository, SpotifyAlbumTracksRepository, SpotifyTrackRepository, YoutubeTrackRepository
from utils import setup_env

class App:
    def __init__(self):
        self.config = setup_env.init_config_with_envs("config.ini")
        self.db = DatabaseManager(self.config)
        self.db.init_db()
        self.spotify_api_client = SpotifyApiClient(self.config).api_client
        self.youtube_api_client = YoutubeApiClient(self.config).api_client
        self._init_repositories()


        self.spotify_scraper = SpotifyScrap(
            api_client=self.spotify_api_client,
            config=self.config,
            repositories=self.repositories,
        )
        self.youtube_scraper = YouTubeScraper(
            api_client=self.youtube_api_client,
            config=self.config,
            repositories=self.repositories,
        )



    def _init_repositories(self):
        class Repositories:
            pass

        self.repositories = Repositories()

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
        self.repositories.youtube_track = YoutubeTrackRepository(
            api_client=self.youtube_api_client,
            session=self.db.session,
            config=self.config,
        )


    def run(self):
        parser = argparse.ArgumentParser()
        parser.add_argument("-spotify_artist_id", help="Spotify Artist ID")
        parser.add_argument("-youtube_channel_id", help="YouTube channel ID")
        args = parser.parse_args()

        if args.spotify_artist_id:
            self.spotify_scraper.main(args.spotify_artist_id)
        
        if args.youtube_channel_id:
            self.youtube_scraper.main(args.youtube_channel_id)


if __name__ == "__main__":
    App().run()

