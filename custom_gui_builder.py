import tkinter as tk
from tkinter import ttk
from test_queries import test_queries
from customtkinter import *


class GUIBuilder:
    def __init__(self, test_builder, conn):
        self.root = CTk()
        self.root.title("Test Creator")
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.frame = CTkFrame(self.root)
        self.frame.pack()
        self.frame.grid_rowconfigure(0, weight=1)
        self.frame.grid_columnconfigure(0, weight=1)
        self.conn = conn
        self.tables = list(map(lambda x: x[0], self.conn.get_tables()))
        self.test_types = list(test_queries.keys())
        self.test_builder = test_builder
        self.initialize_variables()

    def initialize_variables(self):
        self.selected_table = tk.StringVar()
        self.reset_extra_values()

    def reset_extra_values(self):
        self.question_prompts = {}
        self.question_values = {}
        self.question_index = 0
        
    def handle_extra_values(self, event=None):
        self.add_button.configure(state=tk.DISABLED)
        self.finish_button.configure(state=tk.DISABLED)
        selected_test_type_value = self.combo_test_type.get()
        selected_test_type_value_index = self.test_types.index(selected_test_type_value)
        if event is not None:
            self.reset_extra_values()
        if selected_test_type_value_index == 3:  # Change to tests with values
            print("Extra values")
            if (
                len(list(test_queries.get(selected_test_type_value)[1].values()))
                > self.question_index
            ):
                self.question_prompts = list(test_queries.values())[
                    selected_test_type_value_index
                ][1]
                self.value_label.configure(
                    text=list(self.question_prompts.values())[self.question_index]
                )
                self.value_label.grid(row=2, column=3, sticky=tk.W)
                self.value_entry.grid(row=3, column=3, columnspan=1, pady=10)
                self.add_value_test_button.grid(row=4, column=3, columnspan=1)
                return
        self.value_entry.grid_remove()
        self.value_label.grid_remove()
        self.add_value_test_button.grid_remove()
        self.add_button.configure(state=tk.NORMAL)
        self.finish_button.configure(state=tk.DISABLED)

    def get_columns_from_table(self):
        selected_table_value = self.selected_table.get()
        columns = self.conn.get_columns(selected_table_value)
        self.combo_column.configure(values=columns)
        self.reset_extra_values()

    def add_test(self):
        selected_table_value = self.selected_table.get()
        selected_column_value = self.combo_column.get()
        selected_test_type_value = self.test_types.index(self.combo_test_type.get())

        self.test_builder.add_test(
            selected_test_type_value,
            selected_table_value,
            selected_column_value,
            self.question_values,
        )
        self.question_prompts = {}
        self.question_values = {}
        self.question_index = 0
        self.finish_button.configure(state=tk.NORMAL)

    def handle_add_value_test(self):
        self.question_values[
            list(self.question_prompts.keys())[self.question_index]
        ] = self.value_entry.get()
        self.question_index += 1
        self.handle_extra_values(None)
        

    def build_table_checkbox(self, table_frame):
        table_row = 1
        table_column = 0
        for i, table in enumerate(self.tables):
            if i == len(self.tables) // 2:
                table_row = 1
                table_column = 2
            table_checkbox = CTkRadioButton(
                table_frame,
                text=table,
                variable=self.selected_table,
                border_width_checked=3,
                border_width_unchecked=2,
                value=table,
                command=self.get_columns_from_table,
            )
            table_checkbox.grid(row=table_row, column=table_column, sticky=tk.W, pady=5, padx=15)
            table_row += 1

    def build_combobox(self, frame, text, table_row, table_column, values, pad=10):
        combo_label = CTkLabel(frame, text=text)
        combo_label.grid(row=table_row, column=table_column, sticky=tk.W, pady=(pad, 0), padx=pad)
        combobox = CTkComboBox(frame, values=values)
        combobox.grid(row=table_row + 1, column=table_column, pady=(5, pad), padx=pad)
        return combobox

    def create_layout(self):
        instruction_label = CTkLabel(
            self.frame, text="Select table, column, and test type:"
        )
        instruction_label.grid(row=0, column=0, columnspan=2, pady=10)
        table_frame = CTkFrame(self.frame, bg_color="transparent")
        table_frame.grid(row=1, column=0, columnspan=2)
        table_label = CTkLabel(table_frame, text="Table:")
        table_label.grid(row=0, column=0)
        self.build_table_checkbox(table_frame)
        self.combo_column = self.build_combobox(
            self.frame,
            "Column:",
            2,
            0,
            self.conn.get_columns(self.selected_table.get()),
            10
        )
        self.combo_column.set("Column")
        self.combo_test_type = self.build_combobox(
            self.frame, "Test Type:", 2, 1, self.test_types, 10
        )
        self.combo_test_type.configure(command=self.handle_extra_values)

        self.value_label = CTkLabel(self.frame, text="", pady=10, padx=10)
        self.value_label.grid_remove()

        self.value_entry = CTkEntry(self.frame)
        self.value_entry.grid_remove()

        self.add_value_test_button = CTkButton(
            self.frame, text="Add value", command=self.handle_add_value_test
        )
        self.add_value_test_button.grid_remove()
        
        self.add_button = CTkButton(self.frame, text="Add Test", command=self.add_test)
        self.add_button.grid(row=4, column=0, columnspan=1, pady=10)

        self.finish_button = CTkButton(
            self.frame, text="Finish", command=self.root.quit
        )
        self.finish_button.grid(row=4, column=1, columnspan=1)

    def create_tests_gui(self):
        self.create_layout()
        self.root.mainloop()
