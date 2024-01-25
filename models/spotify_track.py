from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey, ARRAY
from .base import Base

class SpotifyTrack(Base):
    __tablename__ = 'spotify_track'
    id = Column(String, primary_key=True)
    artist_id = Column(String, index=True, nullable=False)
    album_id = Column(String, ForeignKey('spotify_album.id'), index=True, nullable=False)
    name = Column(String)
    streams = Column(BigInteger)
    duration = Column(Integer)
    # Spotify not always has full information about release date, so we use string instead of date
    release_date = Column(String)
    popularity = Column(Integer)
    artist_ids = Column(ARRAY(String), index=True)
    cover_url = Column(String)
    url = Column(String)

    def to_dict(self):
        return {
            'id': self.id,
            'artist_id': self.artist_id,
            'album_id': self.album_id,
            'name': self.name,
            'streams': self.streams,
            'duration': self.duration,
            'release_date': self.release_date,
            'popularity': self.popularity,
            'artist_ids': self.artist_ids,
            'cover_url': self.cover_url,
            'url': self.url,
        }