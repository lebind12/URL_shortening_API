from sqlalchemy import Column, Integer, String, Text, DateTime, Identity
from database import Base

class URL(Base):
    __tablename__ = "url_mapping"
    
    shorten_key = Column(String, primary_key=True, nullable=False)
    original_url = Column(String, nullable=False)
    expire_date = Column(DateTime, nullable=True)
    views = Column(Integer, nullable=False)