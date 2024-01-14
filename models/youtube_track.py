from sqlalchemy import Column, Integer, String, DateTime
from .base import Base

class YoutubeTrack(Base):
    __tablename__ = 'youtube_track'
    id = Column(String, primary_key=True)
    channel_id = Column(String, index=True, nullable=False)
    name = Column(String)
    views = Column(Integer)
    release_date = Column(DateTime)
    cover_url = Column(String)
    video_url = Column(String)
    like_count = Column(Integer)

    def to_dict(self):
        return {
            "id": self.id,
            "channel_id": self.channel_id,
            "name": self.name,
            "views": self.views,
            "duration": self.duration,
            "release_date": self.release_date,
            "cover_url": self.cover_url,
            "track_url": self.track_url,
        }