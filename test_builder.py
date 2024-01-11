import os
from db_connection import DB_DAO
import re
from test_queries import test_queries
from gui_builder import GUIBuilder


class SqlTestBuilderInteractive:
    def __init__(self, db_url):
        self.connection = DB_DAO(db_url, False)
        self.tests = {}

    def select_table(self):
        tables = self.get_tables()
        self.clear_screen()
        print("Available tables:")
        for i, table in enumerate(tables, start=1):
            print(f"{i}. {table[0]}")

        choice = int(input("Select a table (number): ")) - 1
        self.tests[tables[choice][0]] = []
        return tables[choice][0]

    def select_column(self, table):
        columns = self.get_columns(table)
        self.clear_screen()
        print(f"Available columns in {table}:")
        for i, column in enumerate(columns, start=1):
            print(f"{i}. {column}")

        choice = int(input("Select a column (number): ")) - 1
        return columns[choice]

    def get_next_file_index(self, directory):
        test_files = [
            file
            for file in os.listdir(directory)
            if file.startswith("test_") and file.endswith(".sql")
        ]
        if not test_files:
            return 1

        return max(int(re.search(r"\d+", file).group()) for file in test_files) + 1

    def save_tests(self, table, dir="tests/"):
        if not os.path.exists(dir):
            os.makedirs(dir)

        table_dir = os.path.join(dir, table)
        if not os.path.exists(table_dir):
            os.makedirs(table_dir)

        index = self.get_next_file_index(table_dir)

        file_name = os.path.join(table_dir, f"test_{index}.sql")
        with open(file_name, "w") as file:
            file.write(f"-- Test {index} for {table}\n")
            file.write(self.last_test + ";\n")

        # tables = list(map(lambda x: x[0], self.get_tables()))

    def create_tests(self, gui=True):
        if gui:
            gui_builder = GUIBuilder(self, self.connection)
            gui_builder.create_tests_gui()
            return
        while True:
            table = self.select_table()
            column = self.select_column(table)
            self.clear_screen()
            print("Available test types:")
            for i, test in enumerate(test_queries.keys(), start=1):
                print(f"{i}. {test}")
            test_type = int(input("Enter test type: \n"))
            self.get_extra_values(test_queries[test_type - 1])
            self.add_test(
                test_type - 1,
                table,
                column,
            )
            if input("Add another test? (y/n): ") == "n":
                break
            else:
                self.clear_screen()

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")
        # print("\033[2J\033[H", end="")  # clear screen

    def format(self, string: str, key, value):
        return string.replace("{" + key + "}", str(value))

    def get_extra_values(self, query_template):
        dict_values = {}
        for variable, question_prompt in query_template[1].items():
            self.clear_screen()
            dict_values[variable] = input(question_prompt + "\n")
        return dict_values

    def build_query(self, query_template, values):
        query = query_template
        for variable, value in values.items():
            query = self.format(query, variable, value)
        return query

    def add_test(self, test_type, table, column, dict_values):
        if len(test_queries.keys()) < test_type:
            print("Invalid test type")
            return
        query_template = list(test_queries.values())[test_type]

        query = query_template[0]

        query = self.format(query, "table", table)
        query = self.format(query, "column", column)

        query = self.build_query(query, dict_values)

        if table in self.tests:
            self.tests[table].append(query)
        else:
            self.tests[table] = [query]
        self.last_test = query
        self.save_tests(table)
