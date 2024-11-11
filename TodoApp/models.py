from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class Todos(Base):
    __table__ = "todos"

    id = Column(Integer, index=True, primary_key=True, autoincrement=True)
    title = Column(String)
    description = Column(String)
    priority = Column(Integer)
    complete = Column(Boolean, default=False)
