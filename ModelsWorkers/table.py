from .base import BaseModelWorker
from Models.tables import Table

class TableModelWorker(BaseModelWorker):
    def __init__(self):
        super().__init__()
    
    def get_tables_by_restaurant(self, restaurant_id: int):
        query_result = self.session.query(Table).filter(Table.restaurant_id == restaurant_id, Table.available == True).all()
        return [piece.toDict() for piece in query_result]