"""Common SQL queries and templates"""


class SQLQueries:
    """Common SQL queries"""

    # Health check
    HEALTH_CHECK = "SELECT 1"

    # Schema operations
    GET_TABLES = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = :schema
    """

    GET_COLUMNS = """
        SELECT column_name, data_type 
        FROM information_schema.columns 
        WHERE table_name = :table AND table_schema = :schema
    """

    # Statistics
    TABLE_SIZE = """
        SELECT pg_size_pretty(pg_total_relation_size(:table))
    """

    ROW_COUNT = """
        SELECT reltuples::bigint AS estimate
        FROM pg_class
        WHERE relname = :table
    """


class SQLTemplates:
    """SQL query templates"""

    INSERT = "INSERT INTO {table} ({columns}) VALUES ({values})"
    UPDATE = "UPDATE {table} SET {set_clause} WHERE {where_clause}"
    DELETE = "DELETE FROM {table} WHERE {where_clause}"
    SELECT = "SELECT {columns} FROM {table} WHERE {where_clause}"
