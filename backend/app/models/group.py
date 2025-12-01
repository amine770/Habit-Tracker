from sqlalchemy import Integer, Text, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base 

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, nullable=False, primary_key=True)
    description = Column(Text, nullable=True)
    name = Column(String, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable=False)
    
    habits = relationship("Habit", back_populates="group")