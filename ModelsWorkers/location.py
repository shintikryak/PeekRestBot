from .base import BaseModelWorker
from Models.locations import Location

class LocationModelWorker(BaseModelWorker):
    def __init__(self):
        super().__init__()
    
    def get_all(self):
        return super().get_all(Location)
