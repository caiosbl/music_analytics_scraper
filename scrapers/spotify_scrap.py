import tqdm
from tqdm import tqdm

SPOTIFY_STREAMS_COUNT_XPATH = '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[1]/div[5]/div/span[4]'

class SpotifyScrap:
    def __init__(self, config, api_client, repositories):
        self.api_client = api_client
        self.chunk_size = config['settings'].getint('spotify.chunk.size')
        self.artist_albums_repository = repositories.spotify_albums
        self.album_tracks_repository = repositories.spotify_album_tracks
        self.track_repository = repositories.spotify_track


    def fetch_artist_albums(self, artist_id):
        self.artist_albums_repository.insert_artist_albums(
            artist_id
        )


    def fetch_albums_tracks(self, artist_id):
        self.album_tracks_repository.insert_artist_album_tracks(
            artist_id
        )


    def fetch_tracks(self, artist_id):
        self.track_repository.insert_tracks(
            artist_id
        )

    
    def get_tracks_streams_by_id(self, tracks_by_id):
        all_track_ids = list(tracks_by_id.keys())

        track_streams_by_id = {}

        with tqdm.tqdm(total=len(tracks_by_id), desc="Getting track streams") as pbar:

            for i in range(0, len(all_track_ids), self.scrapping_max_threads):
                threads = []
                for track_id in all_track_ids[i: i+ self.scrapping_max_threads]:
                    track = tracks_by_id[track_id]
                    #thread = StreamPlaysScrapThread(track, self.web_driver_pool)
                    thread.start()
                    threads.append(thread)

                for thread in threads:
                    thread.join()
                    track_streams_by_id[thread.track["id"]] = thread.streams_count
                    pbar.update(1)

        return track_streams_by_id
    
    def run_scrap(self, artist_id):
        self.fetch_artist_albums(artist_id)
        self.fetch_albums_tracks(artist_id)
        self.fetch_tracks(artist_id)

    
    def main(self, artist_id):
        self.run_scrap(artist_id)
    