from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, Text
from sqlalchemy.orm import relationship
from . import Base

class Submission(Base):
    __tablename__ = "Submission"
    id = Column(Integer, primary_key=True)
    reddit_id = Column(Text, unique=True)
    body = Column(Text)
    title = Column(Text)
    permalink = Column(Text)
    author_id = Column(Integer, ForeignKey('Redditor.id'))
    #authors = relationship("Redditor", primaryjoin="Submission.author_id==Redditor.id", uselist=True, backref="submissions")
    def __init__(self, reddit_id, body, title, permalink, author_id):
        self.reddit_id = reddit_id
        self.body = body
        self.title = title
        self.permalink = permalink
        self.author_id = author_id
