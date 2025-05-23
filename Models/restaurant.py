from sqlalchemy import Column, ForeignKey, Integer, String
from .base import Base
from sqlalchemy.orm import relationship


class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    full_adress = Column(String)
    owner_id = Column(String)
    location_id = Column(Integer, ForeignKey('location.id'))
    location = relationship("Location", backref='restaurants')

    def toDict(self) -> dict:
        return {"id": self.id, "name": self.name}
    
    def init(address, name, owner_id):
        restaurant = Restaurant()
        restaurant.name = name
        restaurant.owner_id = owner_id
        restaurant.full_adress = address
        return restaurant
