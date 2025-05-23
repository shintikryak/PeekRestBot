from .base import BaseModelWorker
from Models.restaurant import Restaurant

class RestaurantModelWorker(BaseModelWorker):
    def __init__(self):
        super().__init__()
    
    def get_restaurant_by_owner(self, id):
        query_result = self.session.query(Restaurant).filter(Restaurant.owner_id==str(id)).first()
        return query_result.toDict()
    
    def get_restaurants_by_location(self, location_id: int):
        query_result = self.session.query(Restaurant).filter(Restaurant.location_id == location_id).all()
        return [piece.toDict() for piece in query_result]

    def get_restaurant_by_id(self, id):
        query_result = self.session.query(Restaurant).filter(Restaurant.id == id).first()
        return query_result
    
    def add_restaurant(self, owner_id, name, address):
        self.session.add(Restaurant.init(address, name, owner_id))
        self.session.commit()
        
