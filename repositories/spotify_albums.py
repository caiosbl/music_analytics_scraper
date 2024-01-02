
from models import SpotifyAlbum
from sqlalchemy.dialects import postgresql

class SpotifyAlbumsRepository:
    def __init__(self, api_client, session, config):
        self.session = session
        self.api_client = api_client
        self.chunk_size = config['settings'].getint('spotify.chunk.size')


    def get_artist_albums(self, artist_id):
        albums = []
        results = None

        print(f"Getting albums from artist {artist_id}...")
        while results is None or len(results) > 0:
            request = self.api_client.artist_albums(
                 artist_id,
                limit=self.chunk_size,
                offset=len(albums),
            )
            results = request.get("items", [])
            albums.extend([
                 SpotifyAlbum(
                      id=album["id"],
                      name=album["name"],
                      artist_id=artist_id,
                ) for album in results
            ])

        return albums


    def insert_artist_albums(self, artist_id):
        albums = self.get_artist_albums(artist_id)
        dict_albums = [album.to_dict() for album in albums]
        raw_insert = postgresql.insert(SpotifyAlbum).values(dict_albums)
        stmt = raw_insert.on_conflict_do_update(
            index_elements=['id'],
            set_={k: raw_insert.excluded[k.name] for k in SpotifyAlbum.__table__.columns if k.name != 'id'}
        )
        self.session.execute(stmt)
        self.session.commit()
        return albums