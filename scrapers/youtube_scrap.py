import openpyxl
from tqdm import tqdm

from api_clients import YoutubeApiClient

class YouTubeScraper:
    def __init__(self, api_client, config, repositories):
        self.api_client = api_client
        self.chunk_size = config['settings'].getint('youtube.chunk.size')
        self.repositories = repositories


    def get_videos(self, channel_id):
        videos = []
        next_page_token = ""

        print(f"Getting videos from channel {channel_id}...")

        while next_page_token is not None:
            request = self.api_client.search().list(
                part="id", channelId=channel_id, maxResults=self.chunk_size, pageToken=next_page_token
            )
            response = request.execute()

            if "items" not in response or not response["items"]:
                break

            video_ids = [item["id"]["videoId"] for item in response["items"] if item["id"].get("videoId")]
            video_details = self.get_video_details(video_ids)
            videos.extend(video_details)

            next_page_token = response.get('nextPageToken')

        return videos

    def get_video_details(self, video_ids):
        videos = []
        for i in range(0, len(video_ids), self.chunk_size):
            video_ids_chunk = video_ids[i:i+self.chunk_size]
            request = self.api_client.videos().list(
                part="snippet,statistics", id=",".join(video_ids_chunk)
            )
            response = request.execute()

            for item in response.get("items", []):
                video_title = item["snippet"]["title"]
                video_date = item["snippet"]["publishedAt"]
                video_views = item["statistics"]["viewCount"]

                videos.append((video_title, video_date, video_views))

        return videos

    def create_spreadsheet(self, videos, filename="youtube_videos.xlsx"):
        print(f"Saving data to {filename}...")
        with tqdm(total=len(videos)) as pbar:
            wb = openpyxl.Workbook()
            sheet = wb.active

            sheet.append(["Title", "Published Date", "Views"])

            for video in videos:
                sheet.append(video)
                pbar.update(1)

            wb.save(filename)
        

    def main(self, channel_id, output_filename="youtube_videos.xlsx"):
        try:
            videos = self.get_videos(channel_id)
            self.create_spreadsheet(videos, output_filename)
        except Exception as e:
            print(f"Erro: {e}")
