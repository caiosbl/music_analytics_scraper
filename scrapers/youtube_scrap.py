class YouTubeScraper:
    def __init__(self, api_client, config, repositories):
        self.api_client = api_client
        self.chunk_size = config['settings'].getint('youtube.chunk.size')
        self.repositories = repositories


    def get_videos(self, channel_id):
        self.repositories.youtube_track.insert_tracks(channel_id)

    def main(self, channel_id):
        self.get_videos(channel_id)

