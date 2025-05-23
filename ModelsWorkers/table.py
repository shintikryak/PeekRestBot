from .base import BaseModelWorker
from Models.tables import Table
from minio_client import MinioClient


class TableModelWorker(BaseModelWorker):
    def __init__(self):
        super().__init__()
    
    def get_tables_by_restaurant(self, restaurant_id: int):
        query_result = self.session.query(Table).filter(Table.restaurant_id == restaurant_id, Table.available == True).all()
        return [piece.toDict() for piece in query_result]
    
    def reserve_table(self, table_id: int):
        self.session.query(Table).filter(Table.id==table_id).update({'available': False})
        self.session.commit()
    
    def add_table(self, restaurant_id, capacity, photo):
        table = Table.init(restaurant_id, capacity, True)
        self.session.add(table)
        self.session.commit()
        MinioClient().add_table(photo, restaurant_id, table.id)
        

