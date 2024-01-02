from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.base import Base

class DatabaseManager:
    def __init__(self, config):
        self.engine = create_engine(config['secrets']['database.url'])
        self.session = sessionmaker(bind=self.engine)()

    def init_db(self):
        Base.metadata.create_all(self.engine)
