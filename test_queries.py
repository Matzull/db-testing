test_queries = {
    # Verificar si una tabla está vacía
    "empty_table": ["SELECT * FROM {table} WHERE NOT EXISTS (SELECT * FROM {table})", {}],

    # Contar filas donde una columna específica no es nula
    "count_non_null": ["SELECT COUNT(*) FROM {table} WHERE {column} IS NOT NULL", {}],

    # Verificar si una columna específica contiene algún valor nulo
    "has_null": ["SELECT * FROM {table} WHERE {column} IS NULL", {}],

    # Contar filas que cumplen una condición específica
    "count_condition": ["SELECT COUNT(*) FROM {table} WHERE {column} = {value}", {"value":"Enter the value to match:"}],

    # Verificar la existencia de un valor específico en una columna
    "value_exists": ["SELECT * FROM {table} WHERE {column} = '{value}'", {"value":"Enter the value to check for existence:"}],

    # Contar filas que están por debajo o por encima de un valor específico
    "count_less_than": ["SELECT COUNT(*) FROM {table} WHERE {column} < {value}", {"value":"Enter the upper limit value:"}],
    "count_greater_than": ["SELECT COUNT(*) FROM {table} WHERE {column} > {value}", {"value":"Enter the lower limit value:"}],

    # Verificar si una columna específica contiene solo valores únicos
    "unique_values": ["SELECT {column}, COUNT(*) FROM {table} GROUP BY {column} HAVING COUNT(*) > 1", {}]
}
