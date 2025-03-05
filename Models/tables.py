from sqlalchemy import Boolean, Column, ForeignKey, Integer
from .base import Base
from sqlalchemy.orm import relationship


class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True)
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship("Restaurant", backref="tables")
    capacity = Column(Integer)
    available = Column(Boolean)

    def toDict(self) -> dict:
        return {"id": self.id, "capacity": self.capacity, "available": self.available}