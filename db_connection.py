from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text


class Connection:
    def __init__(self, db_url, is_postgres=True):
        self.db_url = db_url
        self.is_postgres = is_postgres
        self.engine = create_engine(self.db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def execute_query(self, query):
        with self.get_session() as session:
            result = session.execute(text(query))
            return result.fetchall()

    def get_tables(self):
        return self.execute_query(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND LEFT(table_name, 4) = 'app_' ORDER BY table_name"
            if self.is_postgres
            else "SELECT name FROM sqlite_master WHERE type='table';"
        )

    def get_columns(self, table_name):
        result = self.execute_query(
            f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
            if self.is_postgres
            else f"PRAGMA table_info('{table_name}');"
        )
        return [row[not self.is_postgres] for row in result]
