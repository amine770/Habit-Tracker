from sqlalchemy import Integer, Column, ForeignKey, DateTime, Text
from sqlalchemy.sql.expression import text
from sqlalchemy.orm  import relationship
from app.db.session import Base

class HabitLog(Base):
    __tablename__ = "habit_logs"
    
    id = Column(Integer, nullable=False, primary_key=True)
    habit_id = Column(Integer, ForeignKey("habits.id", ondelete="cascade"), nullable=False)
    completed_at = Column(DateTime(timezone=True), server_default=text("now()"), nullable=False)
    notes = Column(Text, nullable=True)

    habit = relationship("Habit", back_populates="logs")
