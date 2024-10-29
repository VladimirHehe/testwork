from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    avatar = Column(String, index=True)
    gender = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, index=True)
