from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)

    telegram_user_id = Column(Integer, nullable=True)
    instagram_username = Column(String, nullable=True)


