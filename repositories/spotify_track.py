import tqdm
from rich.console import Console
from models import SpotifyTrack, SpotifyAlbumTrack
from sqlalchemy.dialects import postgresql

console = Console()

class SpotifyTrackRepository:
    def __init__(self, api_client, session, config):
        self.session = session
        self.api_client = api_client
        self.chunk_size = config['settings'].getint('spotify.chunk.size')

    def get_tracks(self, artist_id):
        album_tracks = self.session.query(SpotifyAlbumTrack).filter_by(artist_id=artist_id).all()
        tracks = []

        console.print(f"Getting tracks from albums...", style="yellow")

        with tqdm.tqdm(total=len(album_tracks), desc="Fetching all tracks") as pbar:
            for index in range(0, len(album_tracks), self.chunk_size):
                album_tracks_chunk = album_tracks[index:index+self.chunk_size]
                album_tracks_ids = [track.id for track in album_tracks_chunk]
                album_tracks_info = self.api_client.tracks(album_tracks_ids)
                
                for track in album_tracks_info["tracks"]:
                    tracks.append(SpotifyTrack(
                        id=track["uri"],
                        name=track["name"],
                        duration=track["duration_ms"],
                        album_id=track["album"]["id"],
                        release_date=track["album"]["release_date"],
                        popularity=track["popularity"],
                        artist_id=artist_id,
                        artist_ids=[artist["id"] for artist in track["artists"]],
                        cover_url=track["album"]["images"][0]["url"] if track["album"]["images"] else "",
                        url=f"https://open.spotify.com/track/{track['uri'].split(':')[-1]}",
                    ))
            
                pbar.update(len(album_tracks_chunk))

        return tracks


    def insert_tracks(self, artist_id):
        album_tracks = self.get_tracks(artist_id)
        raw_insert = postgresql.insert(SpotifyTrack).values(
            [
                track.to_dict()
                for track in album_tracks
            ]
        )
        stmt = raw_insert.on_conflict_do_update(
            index_elements=['id'],
            set_={k: raw_insert.excluded[k.name] for k in SpotifyTrack.__table__.columns if k.name != 'id'}
        )
        self.session.execute(stmt)
        self.session.commit()
