from models import Artist

class ArtistRepository:
    def __init__(self, session):
        self.session = session


    def insert_artist(self, artist):
        self.session.add(artist)
        self.session.commit()
        return artist

    def get_artist_by_id(self, artist_id):
        return self.session.query(Artist).get(artist_id)
