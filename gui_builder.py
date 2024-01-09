import tkinter as tk
from tkinter import ttk
from test_queries import test_queries
from db_connection import Connection
class GUIBuilder:
    
    def __init__(self, conn):
        self.root = tk.Tk()
        self.root.title("Test Creator")
        style = ttk.Style()
        style.theme_use("clam")
        self.frame = ttk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)
        self.conn = conn
        self.tables = list(map(lambda x: x[0], self.conn.get_tables()))
        self.test_types = list(test_queries.keys())
        self.initialize_variables()
    
    def initialize_variables(self):
        self.selected_table = tk.StringVar()
        self.question_prompts = {}
        self.question_values = {}
        self.question_index = 0
    
    def handle_extra_values(self, _):
        selected_test_type_value = self.combo_test_type.current()
        if selected_test_type_value == 3:  # Change to tests with values
            if len(list(test_queries.values())[selected_test_type_value]) > self.question_index:
                self.question_prompts = list(test_queries.values())[selected_test_type_value][1]
                self.value_label.config(text = list(self.question_prompts.values())[self.question_index])
                self.value_label.grid(row=2, column=3, sticky=tk.W)
                self.value_entry.grid(row=3, column=3, columnspan=1, pady=10)
                self.add_value_test_button.grid(row=4, column=3, columnspan=1)
                return            
        self.value_entry.grid_remove()
        self.value_label.grid_remove()
        self.add_value_test_button.grid_remove()
        self.question_prompts = {}
        self.question_values = {}
        self.question_index = 0

    def get_columns_from_table(self):
        selected_table_value = self.selected_table.get()
        columns = self.conn.get_columns(selected_table_value)
        self.combo_column["values"] = columns
    
    def add_test(self):
        selected_table_value = self.selected_table.get()
        selected_column_value = self.combo_column.current()
        selected_test_type_value = self.test_type.current()
        
        self.add_test(
            selected_test_type_value,
            selected_table_value,
            self.conn.get_columns(selected_table_value)[selected_column_value],
        )
        self.question_prompts = {}
        self.question_values = {}
        self.question_index = 0
    
    def handle_add_value_test(self):
            self.question_values[list(self.question_prompts.keys())[self.question_index]] = self.value_entry.get()
            self.question_index += 1
            self.handle_extra_values(None)
    
    def build_table_checkbox(self, table_frame):
        table_row = 1
        table_column = 0
        for i, table in enumerate(self.tables):
            if i == len(self.tables) // 2:
                table_row = 1
                table_column = 2
            table_checkbox = ttk.Checkbutton(
                table_frame,
                text=table,
                variable=self.selected_table,
                onvalue=table,
                command=self.get_columns_from_table,
            )
            table_checkbox.grid(row=table_row, column=table_column, sticky=tk.W)
            table_row += 1
    
    def build_combobox(self, frame, text, table_row, table_column, values):
        combo_label = ttk.Label(frame, text=text)
        combo_label.grid(row=table_row, column=table_column, sticky=tk.W)
        combobox = ttk.Combobox(frame, values=values)
        combobox.grid(row=table_row + 1, column=table_column)
        return combobox
        
    def create_layout(self):
        instruction_label = ttk.Label(
            self.frame, text="Select table, column, and test type:"
        )
        instruction_label.grid(row=0, column=0, columnspan=2, pady=10)
        table_frame = ttk.Frame(self.frame)
        table_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5)
        table_label = ttk.Label(table_frame, text="Table:")
        table_label.grid(row=0, column=0, sticky=tk.W)
        self.build_table_checkbox(table_frame)
        self.combo_column = self.build_combobox(self.frame, "Column:", 2, 0, self.conn.get_columns(self.selected_table.get()))
        self.combo_test_type = self.build_combobox(self.frame, "Test Type:", 2, 1, self.test_types)
        self.combo_test_type.bind("<<ComboboxSelected>>", self.handle_extra_values)
        
        self.value_label = ttk.Label(self.frame, text="")
        self.value_label.grid_remove()
        
        self.value_entry = ttk.Entry(self.frame)
        self.value_entry.grid_remove()

        self.add_value_test_button = ttk.Button(self.frame, text="Add value", command=self.handle_add_value_test)
        self.add_value_test_button.grid_remove()
        
        self.add_button = ttk.Button(self.frame, text="Add Test", command=self.add_test)
        self.add_button.grid(row=4, column=0, columnspan=1, pady=10)

        self.finish_button = ttk.Button(self.frame, text="Finish", command=self.root.quit)
        self.finish_button.grid(row=4, column=1, columnspan=1)
           
    def create_tests_gui(self):
        self.create_layout()
        self.root.mainloop()