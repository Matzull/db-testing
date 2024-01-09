test_queries = {
    # Check if a table is empty
    "empty_table": [
        "SELECT * FROM {table} WHERE NOT EXISTS (SELECT * FROM {table})",
        {},
    ],
    # Count the number of rows in a table
    "count_non_null": ["SELECT COUNT(*) FROM {table} WHERE {column} IS NOT NULL", {}],
    # Verify that a column has no null values
    "has_null": ["SELECT * FROM {table} WHERE {column} IS NULL", {}],
    # Count the number of rows that match a specific value
    "count_condition": [
        "SELECT COUNT(*) FROM {table} WHERE {column} = {value}",
        {"value": "Enter the value to match:", "column": "Enter the column to match:"}
    ],
    # Verify that a column has a specific value
    "value_exists": [
        "SELECT * FROM {table} WHERE {column} = '{value}'",
        {"value": "Enter the value to check for existence:"},
    ],
    # Count the number of rows that are less than a specific value
    "count_less_than": [
        "SELECT COUNT(*) FROM {table} WHERE {column} < {value}",
        {"value": "Enter the limit value:"},
    ],
    "count_greater_than": [
        "SELECT COUNT(*) FROM {table} WHERE {column} > {value}",
        {"value": "Enter the limit value:"},
    ],
    # Verify that a column has a unique values
    "unique_values": [
        "SELECT {column}, COUNT(*) FROM {table} GROUP BY {column} HAVING COUNT(*) > 1",
        {},
    ],
}
