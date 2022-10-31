from sqlalchemy import Column, Integer, String, Float, Text

from db import Base


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    description = Column(Text)
