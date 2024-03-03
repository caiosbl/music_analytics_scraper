from sqlalchemy import Column, BigInteger, String, DateTime
from .base import Base

class YoutubeTrack(Base):
    __tablename__ = 'youtube_track'
    id = Column(String, primary_key=True)
    channel_id = Column(String, index=True, nullable=False)
    name = Column(String)
    views = Column(BigInteger)
    release_date = Column(DateTime)
    cover_url = Column(String)
    like_count = Column(BigInteger)

    @property
    def streams(self):
        return self.views

    def to_dict(self):
        return {
            "id": self.id,
            "channel_id": self.channel_id,
            "name": self.name,
            "views": self.views,
            "release_date": self.release_date,
            "cover_url": self.cover_url,
            "like_count": self.like_count,
        }
