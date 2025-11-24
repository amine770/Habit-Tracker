from sqlalchemy import String, Integer, Column, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql import func
from app.db.session import Base

class Habit(Base):
    __tablename__ = "habits"

    id = Column(Integer, nullable= False, primary_key= True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="cascade"), nullable= False)
    name = Column(String, nullable= False, unique= True)
    description = Column(Text, nullable= True )
    frequency = Column(String, server_default="daily")
    color = Column(String, server_default="blue")
    icon = Column(String, nullable=True)
    is_active = Column(Boolean, server_default=text("true"))
    created_at = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=text("now()"), onupdate=func.now(), nullable=False)

    user = relationship("User")
