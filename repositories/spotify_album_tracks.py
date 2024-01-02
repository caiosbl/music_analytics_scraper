import tqdm
from models import SpotifyAlbumTrack, SpotifyAlbum
from sqlalchemy import insert
from sqlalchemy.dialects import postgresql

class SpotifyAlbumTracksRepository:
    def __init__(self, api_client, session, config):
        self.session = session
        self.api_client = api_client
        self.chunk_size = config['settings'].getint('spotify.chunk.size')


    def get_albums_tracks(self, artist_id):
        albums = self.session.query(SpotifyAlbum).filter_by(artist_id=artist_id).all()
        albums_tracks = []
        with tqdm.tqdm(total=len(albums), desc="Getting musics from albums") as pbar:
            for album in albums:
                albums_tracks.extend(self.get_album_tracks(album))
                pbar.update(1)

        return albums_tracks


    def get_album_tracks(self, album):
        album_tracks = []
        results = None
        while results is None or len(results) > 0:
            request = self.api_client.album_tracks(
                album_id=album.id,
                limit=self.chunk_size,
                offset=len(album_tracks),
            )
            results = request.get("items", [])
            album_tracks.extend([
                SpotifyAlbumTrack(
                    id=track["id"],
                    artist_id=album.artist_id,
                    album_id=album.id,
                    
                )
                for track in results
            ])

        return album_tracks

    def insert_artist_album_tracks(self, artist_id):
        album_tracks = self.get_albums_tracks(artist_id)
        raw_insert = postgresql.insert(SpotifyAlbumTrack).values(
            [
                track.to_dict()
                for track in album_tracks
            ]
        
        )
        stmt = raw_insert.on_conflict_do_update(
            index_elements=['id'],
            set_={k: raw_insert.excluded[k.name] for k in SpotifyAlbumTrack.__table__.columns if k.name != 'id'}
        )
        self.session.execute(stmt)
        self.session.commit()