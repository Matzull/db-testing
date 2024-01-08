from db_connection import Connection
from test_queries import test_queries
from config import api_openai_key, database_url
import json
import requests
from tqdm import tqdm


class SmartQuery:
    def __init__(self, db_url):
        self.connection = Connection(db_url)

    def get_schema(self):
        schema = []
        # Get tables
        tables = self.connection.execute_query(
            """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
            ORDER BY table_schema, table_name;
        """
        )
        app_tables = []
        # Get columns
        for table in tqdm(tables):
            _, table_name = table
            if not table_name.startswith("app_"):
                continue
            else:
                app_tables.append(table_name)
            schema.append(f"Table: {table_name}\n")
            schema.append("  Columns: ")
            columns = self.connection.execute_query(
                f"""
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position;
            """
            )
            for column in columns[:-1]:
                schema.append(f"{column[0]}, ")
            schema.append(f"{columns[-1][0]}\n")

            # Get foreign keys
            schema.append("  Foreign keys:\n")
            foreign_keys = self.connection.execute_query(
                f"""
                SELECT tc.constraint_name, kcu.column_name, ccu.table_schema AS foreign_table_schema, 
                    ccu.table_name AS foreign_table_name, ccu.column_name AS foreign_column_name 
                FROM 
                    information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                    ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage AS ccu
                    ON ccu.constraint_name = tc.constraint_name
                WHERE tc.table_name = '{table_name}' AND tc.constraint_type = 'FOREIGN KEY';
            """
            )

            for fk in foreign_keys:
                schema.append(f"    {fk[1]} -> {fk[3]}({fk[4]})\n")

            schema.append("\n")
        return app_tables, "".join(schema)

    def print_schema(self):
        print(self.get_schema()[1])

    def call_chatgpt(self, data, debug=False, retries=5, wait_time=2):
        if retries == 0:
            print("max retries exceeded for this request due to connection error")
            return ""

        headers = {
            "Authorization": f"Bearer {api_openai_key}",
            "Content-Type": "application/json",
        }

        try:
            # print(f"calling chatgpt api... {wait_time}s wait time")
            # time.sleep(wait_time)
            with requests.Session() as s:
                response = s.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers=headers,
                    json=data,
                )

                if response.status_code == 200:
                    print("Success!")
                    x = json.loads(response.text)["choices"][0]["message"]["content"]
                    return x
                else:
                    if debug:
                        print(response.content)
                    else:
                        print("Failed request status:", response.status_code)

        except Exception as e:
            print(e)
            return self.call_chatgpt(data, retries - 1, wait_time * wait_time)

    def get_queries_ai(self):
        schema = self.get_schema()
        json_data = json_data = {
            "model": "gpt-3.5-turbo-1106",
            "messages": [
                {
                    "role": "system",
                    "content": f"You are an SQL expert. You are given this database schema {schema[1]} Your task is to write error checking queries that must return 0 rows if no error was found and the rows that contain errors otherwise",
                },
                {
                    "role": "user",
                    "content": f"Using the schema please write the error checking queries you consider important for the table {schema[0][1]}.",
                },
            ],
        }
        response = self.call_chatgpt(json_data, debug=True)
        print(response)
        return test_queries


sq = SmartQuery(database_url)
# sq.get_queries_ai()
sq.print_schema()
