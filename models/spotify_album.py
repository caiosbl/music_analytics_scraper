from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class SpotifyAlbum(Base):
    __tablename__ = 'spotify_album'
    id = Column(String, primary_key=True)
    artist_id = Column(String, index=True, nullable=False)
    name = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'name': self.name,
        }