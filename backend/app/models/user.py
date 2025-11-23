from app.db.base import Base
from sqlalchemy import String, Integer, Column, DateTime
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, nullable=False, primary_key=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False)

    habit = relationship("Habit", back_populates="user")