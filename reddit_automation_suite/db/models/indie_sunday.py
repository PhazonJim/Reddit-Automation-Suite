from sqlalchemy import ForeignKey
from sqlalchemy import Column, Integer, Text, Boolean
from sqlalchemy.orm import relationship
from . import Base


class IndieSunday(Base):
    __tablename__ = "IndieSunday"
    id = Column(Integer, primary_key=True)
    submission_id = Column(Integer, ForeignKey("Submission.id"), unique=True)
    hub_id = Column(Text)
    approved = Column(Boolean)
    # submissions = relationship("Submission", primaryjoin="IndieSunday.submission_id==Submission.reddit_id", uselist=True, backref="indiesunday")
    def __init__(self, submission_id, hub_id, approved):
        self.submission_id = submission_id
        self.hub_id = hub_id
        self.approved = approved
