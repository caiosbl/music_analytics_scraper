import googleapiclient.discovery
import googleapiclient.errors

class YoutubeApiClient:
    def __init__(self, config):
        youtube_api_key = config['secrets']['youtube.api.key']
        api_service_name = config['settings']['youtube.api.service.name']
        api_version = config['settings']['youtube.api.version']

        self.api_client = googleapiclient.discovery.build(api_service_name, api_version, developerKey=youtube_api_key)