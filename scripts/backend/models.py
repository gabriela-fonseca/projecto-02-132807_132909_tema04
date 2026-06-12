from sqlalchemy import Column, Integer, String, Float
from database import Base

class Media(Base):
    __tablename__ = "media"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    media_type = Column(String)
    description = Column(String)
    poster_url = Column(String)
    rating = Column(Float)