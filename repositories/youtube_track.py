import tqdm
from models import YoutubeTrack
from sqlalchemy.dialects import postgresql
from rich.console import Console

console = Console()

class YoutubeTrackRepository:
    def __init__(self, api_client, session, config):
        self.session = session
        self.api_client = api_client
        self.chunk_size = config['settings'].getint('youtube.chunk.size')

    def get_videos_by_id(self, channel_id):
        video_ids = []
        videos = []
        next_page_token = ""

        console.print(f"Getting videos from channel {channel_id}...", style="yellow")

        while next_page_token is not None:
            request = self.api_client.search().list(
                part="id", channelId=channel_id, maxResults=self.chunk_size, pageToken=next_page_token
            )
            response = request.execute()

            if "items" not in response or not response["items"]:
                break

            video_ids.extend([item["id"]["videoId"] for item in response["items"] if item["id"].get("videoId")])
            next_page_token = response.get('nextPageToken')

        
        with tqdm.tqdm(total=len(video_ids), desc="Fetching all videos") as pbar:
            for index in range(0, len(video_ids), self.chunk_size):
                video_ids_chunk = video_ids[index:index+self.chunk_size]
                video_details = self.get_video_details(video_ids_chunk)
                videos.extend(video_details)
                pbar.update(len(video_ids_chunk))

        return {
            video.id: video
            for video in videos
        }

    def get_video_details(self, video_ids):
        videos = []
        request = self.api_client.videos().list(
            part="snippet,statistics", id=",".join(video_ids)
        )
        response = request.execute()

        for item in response.get("items", []):
            videos.append(YoutubeTrack(
                id=item["id"],
                channel_id=item["snippet"]["channelId"],
                name=item["snippet"]["title"],
                release_date=item["snippet"]["publishedAt"],
                like_count=item["statistics"].get("likeCount"),
                views=item["statistics"]["viewCount"],
                cover_url=item["snippet"]["thumbnails"]["default"]["url"],
            ))

        return videos


    def insert_tracks(self, channel_id):
        tracks_by_id = self.get_videos_by_id(channel_id)

        raw_insert = postgresql.insert(YoutubeTrack).values(
            [
                track.to_dict()
                for track in tracks_by_id.values()
            ]
        )
        stmt = raw_insert.on_conflict_do_update(
            index_elements=['id'],
            set_={k: raw_insert.excluded[k.name] for k in YoutubeTrack.__table__.columns if k.name != 'id'}
        )
        self.session.execute(stmt)
        self.session.commit()
