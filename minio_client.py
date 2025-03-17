from minio import Minio
from io import BytesIO

class MinioClient:
    def __init__(self):
        self.client = Minio(
            "localhost:9000",
            "minioadmin",
            "minioadmin",
            secure=False
        )
    
    def get_tables_by_rest(self, restaurant: str):
        objects = self.client.list_objects("tables", recursive=True)
        photos = []
        for obj in objects:
             #if restaurant in obj.object_name:
            data = self.client.get_object("tables", obj.object_name)
            photos.append(BytesIO(data.read()))
        return photos