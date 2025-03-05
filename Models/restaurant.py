from sqlalchemy import Column, ForeignKey, Integer, String
from .base import Base
from sqlalchemy.orm import relationship


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    full_adress = Column(String)
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location", backref='restaurants')

    def toDict(self) -> dict:
        return {"id": self.id, "name": self.name}
