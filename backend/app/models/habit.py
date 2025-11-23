from sqlalchemy import String, Integer, Column, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
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
    is_active = Column(bool, server_default=True)
    created_at = Column(DateTime(timezone=True), server_default=text("now()"))
    update_at = Column(DateTime(timezone=True), server_default=text("now()"))

    user = relationship("User", back_populates="habits")
