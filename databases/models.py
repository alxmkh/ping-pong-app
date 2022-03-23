from sqlalchemy import Column, Integer

from .database import Base


class Ping(Base):
    __tablename__ = "ping_count"
    id = Column(Integer, primary_key=True, index=True)
    ping_counter = Column(Integer)
