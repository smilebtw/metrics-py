from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

# Cold Data
class Channel(Base):
    __tablename__ = 'channels'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    channelId = Column(String, unique=True)
    channelName = Column(String)
    channelLabel = Column(String)
    createdAt = Column(DateTime, default=datetime.utcnow)
    updatedAt = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    videos = relationship('Video', back_populates='channel')

# Cold Data
class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    videoId = Column(String)
    videoTitle = Column(String)
    publishedAt = Column(DateTime)
    channelId = Column(Integer, ForeignKey('channels.id'))

    channel = relationship('Channel', back_populates='videos')

# Hot Data
class VideoMetrics(Base):
    __tablename__ = 'videoMetrics'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    videoId = Column(String, ForeignKey('videos.videoId'))
    channelId = Column(String, ForeignKey('channels.channelId'))
    videoViews = Column(Integer)
    videoLikes = Column(Integer)
    videoComments = Column(Integer)
    createdAt = Column(DateTime, default=datetime.utcnow)
    
# Hot Data
class ChannelMetrics(Base):
    __tablename__ = 'channelMetrics'

    metricsId = Column(Integer, primary_key=True, autoincrement=True, index=True)
    channelId = Column(String, ForeignKey('channels.channelId'))
    subscribers = Column(Integer)
    views = Column(Integer)
    comments = Column(Integer)
    likes = Column(Integer)
    metricsDate = Column(DateTime, default=datetime.utcnow)

