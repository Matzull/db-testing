from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from configparser import ConfigParser
from sqlalchemy.sql import text


class Connection:
    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def execute_query(self, query):
        with self.get_session() as session:
            result = session.execute(text(query))
            return result.fetchall()
