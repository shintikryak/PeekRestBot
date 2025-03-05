from sqlalchemy import Column, Integer, String
from .base import Base

class Location(Base):
    __tablename__ = "location"

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def toDict(self) -> dict:
        return {"id": self.id, "name": self.name}
