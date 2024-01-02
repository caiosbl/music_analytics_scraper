from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class SpotifyAlbumTrack(Base):
    __tablename__ = 'spotify_album_track'
    id = Column(String, primary_key=True)
    artist_id = Column(String, index=True, nullable=False)
    album_id = Column(String, ForeignKey('spotify_album.id'), index=True, nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'album_id': self.album_id,
        }
