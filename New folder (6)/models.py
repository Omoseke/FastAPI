from sqlalchemy import Column, Integer, String, Boolean, Date
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    date_of_birth = Column(Date)
    country = Column(String)
    favorite_sport = Column(String)
    favorite_team = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=False)
