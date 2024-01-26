from models import SpotifyTrack
from services import WebDriverPool, StreamPlaysScrapThread
from tqdm import tqdm
from queue import Queue

class SpotifyStreamsRepository:
    def __init__(self, api_client, session, config):
        self.session = session
        self.api_client = api_client
        self.scrapping_max_threads = config['settings'].getint('spotify.scrapping.max_threads')
        self.implicitly_wait = config['settings'].getint('spotify.scrapping.implicitly_wait')
        self.web_driver_pool = WebDriverPool(
            size=self.scrapping_max_threads,
            webdriver_chromium_path=config['settings']['chromium.binary.path'],
            webdriver_path=config['settings']['chromium.driver.path']
        )


    def get_tracks_streams(self, tracks):
        tracks_with_streams = []
        failed_threads = Queue()
        with tqdm(total=len(tracks), desc="Getting track streams") as pbar:
            for i in range(0, len(tracks), self.scrapping_max_threads):
                threads = []
                for track in tracks[i: i+ self.scrapping_max_threads]:
                    thread = StreamPlaysScrapThread(track, self.web_driver_pool, self.implicitly_wait)
                    thread.start()
                    threads.append(thread)
                for thread in threads:
                    try:
                        thread.join()
                        tracks_with_streams.append(thread.track)
                        pbar.update(1)
                    except Exception as e:
                        failed_threads.put(thread)


            while not failed_threads.empty():
                thread = failed_threads.get()
                thread.run()
                tracks_with_streams.append(thread.track)
                pbar.update(1)

                    
        return tracks_with_streams

    def insert_tracks_stream_counts(self, artist_id):
        tracks = self.session.query(SpotifyTrack).filter_by(artist_id=artist_id).all()
        tracks_with_streams = self.get_tracks_streams(tracks)

        for track in tracks_with_streams:
            self.session.add(track)

        self.session.commit()
