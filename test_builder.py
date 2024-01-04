import os
from db_connection import Connection
import re
from test_queries import test_queries


class SqlTestBuilderInteractive:
    def __init__(self, db_url):
        self.connection = Connection(db_url)
        self.tests = {}
        self.current_table = None
        self.current_column = None

    def get_tables(self):
        return self.connection.execute_query(
            "SELECT name FROM sqlite_master WHERE type='table';"
        )

    def get_columns(self, table_name):
        result = self.connection.execute_query(f"PRAGMA table_info({table_name});")
        return [row[1] for row in result]

    def select_table(self):
        tables = self.get_tables()
        self.clear_screen()
        print("Available tables:")
        for i, table in enumerate(tables, start=1):
            print(f"{i}. {table[0]}")

        choice = int(input("Select a table (number): ")) - 1
        self.current_table = tables[choice][0]
        self.tests[self.current_table] = []

    def select_column(self):
        columns = self.get_columns(self.current_table)
        self.clear_screen()
        print(f"Available columns in {self.current_table}:")
        for i, column in enumerate(columns, start=1):
            print(f"{i}. {column}")

        choice = int(input("Select a column (number): ")) - 1
        self.current_column = columns[choice]

    def get_next_file_index(self, directory):
        test_files = [
            file
            for file in os.listdir(directory)
            if file.startswith("test_") and file.endswith(".sql")
        ]
        if not test_files:
            return 1

        return max(int(re.search(r"\d+", file).group()) for file in test_files) + 1

    def save_tests(self, dir="tests/"):
        if not os.path.exists(dir):
            os.makedirs(dir)

        table_dir = os.path.join(dir, self.current_table)
        if not os.path.exists(table_dir):
            os.makedirs(table_dir)

        index = self.get_next_file_index(table_dir)

        file_name = os.path.join(table_dir, f"test_{index}.sql")
        with open(file_name, "w") as file:
            file.write(f"-- Test {index} for {self.current_table}\n")
            file.write(self.last_test + ";\n")

    def create_tests(self):
        while True:
            self.select_table()
            self.select_column()
            self.clear_screen()
            print("Available test types:")
            for i, test in enumerate(test_queries.keys(), start=1):
                print(f"{i}. {test}")
            test_type = int(input("Enter test type: \n"))
            self.add_test(test_type - 1)
            if input("Add another test? (y/n): ") == "n":
                break

    def clear_screen(self):
        print("\033[2J\033[H", end="")  # clear screen

    def format(self, string: str, key, value):
        return string.replace("{" + key + "}", str(value))

    def add_test(self, test_type):
        if len(test_queries.keys()) < test_type:
            print("Invalid test type")
            return
        query_template = list(test_queries.values())[test_type]

        query = query_template[0]

        query = self.format(query, "table", self.current_table)
        query = self.format(query, "column", self.current_column)
        for variable, question_prompt in query_template[1].items():
            self.clear_screen()
            print("Query is:", query, end="\n\n")
            query = self.format(query, variable, input(question_prompt + "\n"))

        self.tests[self.current_table].append(query)
        self.last_test = query
        self.save_tests()
