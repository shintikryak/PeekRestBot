import io
from PIL import Image
from minio import Minio, S3Error
from io import BytesIO

class MinioClient:
    def __init__(self):
        self.client = Minio(
            "localhost:9000",
            "minioadmin",
            "minioadmin",
            secure=False
        )
    
    def get_tables_by_rest(self, restaurant: str, tables):
        objects = self.client.list_objects("tables", recursive=True, prefix=restaurant + "/")
        photos = []
        for obj in objects:
            try:
            # Получаем объект из MinIO
                data = self.client.get_object("tables", obj.object_name)
                photo_data = data.read()  # Читаем данные ОДИН раз
                data.close()  # Важно: закрываем соединение
                
                # Проверяем, что данные не пустые
                if not photo_data:
                    print(f"[WARN] Пустые данные для {obj.object_name}")
                    continue
                    
                # Проверяем валидность изображения
                img = Image.open(BytesIO(photo_data))
                img.verify()  # Дополнительная проверка целостности
                
                # Добавляем в список НОВЫЙ BytesIO с теми же данными
                photos.append(BytesIO(photo_data))  # Используем уже прочитанные данные
            
            except Exception as e:
                print(f"[ERROR] Ошибка при обработке {obj.object_name}: {str(e)}")
                continue
        return photos

    def add_table(self, photo_bytes, restaurant, table_id):
        try:
            self.client.put_object(
                bucket_name="tables",
                object_name=str(restaurant) + "/" + str(table_id) + ".jpg",
                data=io.BytesIO(photo_bytes),
                length=len(photo_bytes),
                content_type="image/jpeg"
            )
            print(f"Файл успешно загружен в " + str(table_id) + ".jpg")
        except S3Error as e:
            print(f"Ошибка при загрузке: {e}")