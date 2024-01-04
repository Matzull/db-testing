from db_connection import Connection
from test_queries import test_queries


class SmartQuery:
    def __init__(self, db_url):
        self.connection = Connection(db_url)
    
    def get_schema(self):
        return self.connection.execute_query(
            "PRAGMA table_info(albums);"
        )
    
    def print_schema(self):
        for table in self.get_schema()[0]:
            print(table)

sq = SmartQuery("sqlite:///chinook.db")
sq.print_schema()