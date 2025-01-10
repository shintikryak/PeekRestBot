from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class BaseModelWorker:
    def __init__(self):
        try:
            engine = create_engine("postgresql://user:password@localhost:5432/peek-rest", echo=True)
            Session = sessionmaker(bind=engine)
            self.session = Session()
        except Exception as e:
            print("some error occured: ", e)
    
    def get_all(self, this_type):
        query_result = self.session.query(this_type).all()
        return [piece.toDict() for piece in query_result]
