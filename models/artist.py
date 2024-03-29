from sqlalchemy import Column, String, Integer, DateTime
from .base import Base

class Artist(Base):
    __tablename__ = 'artist'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    spotify_id = Column(String, nullable=True)
    youtube_id = Column(String, nullable=True)
    deezer_id = Column(String, nullable=True)
    apple_music_id = Column(String, nullable=True)
    amazon_music_id = Column(String, nullable=True)
    tidal_id = Column(String, nullable=True)
    last_stats_update = Column(DateTime, nullable=True)


    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'spotify_id': self.spotify_id,
            'youtube_id': self.youtube_id,
            'deezer_id': self.deezer_id,
            'apple_music_id': self.apple_music_id,
            'amazon_music_id': self.amazon_music_id,
            'tidal_id': self.tidal_id,
        }

