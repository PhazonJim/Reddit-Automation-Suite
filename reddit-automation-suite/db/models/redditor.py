from sqlalchemy import Column, Integer, Text
from . import Base

class Redditor(Base):
    __tablename__ = "Redditor"
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    def __init__(self, name):
        self.name = name