import os
from db_connection import Connection
import re
from test_queries import test_queries
import tkinter as tk
from tkinter import ttk


class SqlTestBuilderInteractive:
    def __init__(self, db_url):
        self.connection = Connection(db_url)
        self.tests = {}

    def get_tables(self):
        return self.connection.execute_query(
            #"SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND LEFT(table_name, 4) = 'app_' ORDER BY table_name"
             "SELECT name FROM sqlite_master WHERE type='table';"
        )

    def get_columns(self, table_name):
        result = self.connection.execute_query(
            #f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'"
            f"PRAGMA table_info('{table_name}');"
        )
        return [row[1] for row in result]

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

    def create_tests_gui(self):
        # Crear la ventana principal
        root = tk.Tk()
        root.title("Test Creator")

        # Establecer el estilo para mejorar la apariencia
        style = ttk.Style()
        style.theme_use("clam")

        # Inicializar las variables para almacenar las listas de tablas y tipos de prueba
        tables = list(map(lambda x: x[0], self.get_tables()))
        test_types = list(test_queries.keys())

        # Variables para almacenar las selecciones
        selected_table = tk.StringVar()
        selected_column = tk.StringVar()

        # Función para mostrar u ocultar el campo de texto según la selección del combobox
        def show_hide_test_details(event):
            selected_test_type_value = test_combobox.current()
            if selected_test_type_value == 0:  # Cambia "Custom" al valor deseado
                value_label.config(text = "Enter value:")
                value_label.grid(row=table_row + 3, column=3, sticky=tk.W)
                test_details_entry.grid(row=table_row + 4, column=3, columnspan=2, pady=10)
                add_value_test_button.grid(row=table_row + 5, column=3, columnspan=2)
            else:
                test_details_entry.grid_remove()

        def load_columns():
            selected_table_value = selected_table.get()
            columns = self.get_columns(selected_table_value)
            column_combobox["values"] = columns

        # Botón para agregar el test
        def add_test():
            selected_table_value = selected_table.get()
            selected_column_value = column_combobox.current()
            selected_test_type_value = test_combobox.current()
            
            self.add_test(
                selected_test_type_value,
                selected_table_value,
                self.get_columns(selected_table_value)[selected_column_value],
            )

        # Crear un marco para organizar los elementos de manera más limpia
        frame = ttk.Frame(root)
        frame.pack(padx=20, pady=20)

        # Etiqueta de instrucción
        instruction_label = ttk.Label(
            frame, text="Select table, column, and test type:"
        )
        instruction_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Checkboxes para seleccionar la tabla en varias columnas
        table_label = ttk.Label(frame, text="Table:")
        table_label.grid(row=1, column=0, sticky=tk.W)

        table_row = 1
        table_column = 1
        for i, table in enumerate(tables):
            if i == len(tables) // 2:
                table_row = 1
                table_column = 2
            table_checkbox = ttk.Checkbutton(
                frame,
                text=table,
                variable=selected_table,
                onvalue=table,
                command=load_columns,
            )
            table_checkbox.grid(row=2 + table_row, column=table_column, sticky=tk.W)
            table_row += 1

        # Combobox para seleccionar la columna
        column_label = ttk.Label(frame, text="Column:")
        column_label.grid(row=table_row + 3, column=1, sticky=tk.W)
        column_combobox = ttk.Combobox(frame, values=self.get_columns(selected_table.get()))
        column_combobox.grid(row=table_row + 4, column=1)

        # Combobox para seleccionar el tipo de prueba
        test_label = ttk.Label(frame, text="Test Type:")
        test_label.grid(row=table_row + 3, column=2, sticky=tk.W)
        test_combobox = ttk.Combobox(frame, values=test_types)
        test_combobox.grid(row=table_row + 4, column=2, columnspan=2, sticky=tk.W)
        test_combobox.bind("<<ComboboxSelected>>", show_hide_test_details)

        # Campo de texto para ingresar detalles del test (inicialmente oculto)
        # dict_values = {}
        # def handle_add_value_test(event):
        #     dict_values = list(test_queries.values())[test_type][1].items()[question_index] = test_details_entry.get()
        #     question_index += 1
        
        value_label = ttk.Label(frame, text="")
        value_label.grid_remove()
        
        test_details_entry = ttk.Entry(frame)
        test_details_entry.grid_remove()

        question_index = 0
        add_value_test_button = ttk.Button(frame, text="Add value", command=None)
        add_value_test_button.grid_remove()
        
        # Botón para agregar el test
        add_button = ttk.Button(frame, text="Add Test", command=add_test)
        add_button.grid(row=table_row + 5, column=0, columnspan=2, pady=10)

        # Botón para finalizar
        finish_button = ttk.Button(frame, text="Finish", command=root.quit)
        finish_button.grid(row=table_row + 5, column=1, columnspan=2)

        # Ejecutar la interfaz gráfica
        root.mainloop()
    
    def create_tests(self, gui=True):
        if gui:
            self.create_tests_gui()
            return
        while True:
            table = self.select_table()
            column = self.select_column(table)
            self.clear_screen()
            print("Available test types:")
            for i, test in enumerate(test_queries.keys(), start=1):
                print(f"{i}. {test}")
            test_type = int(input("Enter test type: \n"))
            self.add_test(test_type - 1, table, column)
            if input("Add another test? (y/n): ") == "n":
                break
            else:
                self.clear_screen()

    def clear_screen(self):
        os.system("cls" if os.name == "nt" else "clear")
        # print("\033[2J\033[H", end="")  # clear screen

    def format(self, string: str, key, value):
        return string.replace("{" + key + "}", str(value))

    def add_test(self, gui, test_type, table, column):
        if len(test_queries.keys()) < test_type:
            print("Invalid test type")
            return
        query_template = list(test_queries.values())[test_type]

        query = query_template[0]

        query = self.format(query, "table", table)
        query = self.format(query, "column", column)
        for variable, question_prompt in query_template[1].items():
            self.clear_screen()
            print("Query is:", query, end="\n\n")
            query = self.format(query, variable, input(question_prompt + "\n"))

        if table in self.tests:
            self.tests[table].append(query)
        else:
            self.tests[table] = [query]
        self.last_test = query
        self.save_tests(table)
