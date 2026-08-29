"""
SQL Environment & Database Integration Module
Provides functions for connecting to SQLite database and loading data.
"""

import pandas as pd
import sqlite3
from pathlib import Path
from typing import Optional, List, Dict
import json


def create_connection(db_path: str = None) -> sqlite3.Connection:
    """
    Create SQLite database connection.
    
    Args:
        db_path: Path to SQLite database (None for in-memory)
    
    Returns:
        SQLite connection object
    """
    if db_path is None:
        return sqlite3.connect(':memory:')
    return sqlite3.connect(db_path)


def create_tables_from_dataframes(conn: sqlite3.Connection, 
                                   dataframes: Dict[str, pd.DataFrame],
                                   prefix: str = '') -> List[str]:
    """
    Create tables from DataFrames.
    
    Args:
        conn: SQLite connection
        dataframes: Dictionary of table_name -> DataFrame
        prefix: Table name prefix
    
    Returns:
        List of created table names
    """
    tables = []
    for name, df in dataframes.items():
        table_name = f"{prefix}{name}" if prefix else name
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        tables.append(table_name)
    return tables


def get_table_info(conn: sqlite3.Connection, table_name: str) -> Dict:
    """
    Get table information.
    
    Args:
        conn: SQLite connection
        table_name: Name of the table
    
    Returns:
        Dictionary with table information
    """
    cursor = conn.cursor()
    
    # Get column info
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    
    # Get row count
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    row_count = cursor.fetchone()[0]
    
    return {
        'table_name': table_name,
        'columns': [{'name': col[1], 'type': col[2], 'notnull': col[3]} for col in columns],
        'row_count': row_count
    }


def list_tables(conn: sqlite3.Connection) -> List[str]:
    """
    List all tables in the database.
    
    Args:
        conn: SQLite connection
    
    Returns:
        List of table names
    """
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    return [row[0] for row in cursor.fetchall()]


def execute_query(conn: sqlite3.Connection, query: str) -> pd.DataFrame:
    """
    Execute SQL query and return results as DataFrame.
    
    Args:
        conn: SQLite connection
        query: SQL query to execute
    
    Returns:
        DataFrame with query results
    """
    return pd.read_sql_query(query, conn)


def get_database_stats(conn: sqlite3.Connection) -> Dict:
    """
    Get database statistics.
    
    Args:
        conn: SQLite connection
    
    Returns:
        Dictionary with database statistics
    """
    tables = list_tables(conn)
    stats = {
        'total_tables': len(tables),
        'tables': {}
    }
    
    for table in tables:
        stats['tables'][table] = get_table_info(conn, table)
    
    return stats


def load_csv_to_table(conn: sqlite3.Connection, csv_path: str, table_name: str) -> int:
    """
    Load CSV file into database table.
    
    Args:
        conn: SQLite connection
        csv_path: Path to CSV file
        table_name: Name of the table to create
    
    Returns:
        Number of rows loaded
    """
    df = pd.read_csv(csv_path)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    return len(df)


def export_table_to_csv(conn: sqlite3.Connection, table_name: str, csv_path: str) -> int:
    """
    Export database table to CSV file.
    
    Args:
        conn: SQLite connection
        table_name: Name of the table
        csv_path: Path to output CSV file
    
    Returns:
        Number of rows exported
    """
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    df.to_csv(csv_path, index=False)
    return len(df)


def create_view(conn: sqlite3.Connection, view_name: str, query: str) -> None:
    """
    Create a database view.
    
    Args:
        conn: SQLite connection
        view_name: Name of the view
        query: SQL query for the view
    """
    cursor = conn.cursor()
    cursor.execute(f"CREATE VIEW IF NOT EXISTS {view_name} AS {query}")
    conn.commit()


def get_sqlite_version(conn: sqlite3.Connection) -> str:
    """
    Get SQLite version.
    
    Args:
        conn: SQLite connection
    
    Returns:
        SQLite version string
    """
    cursor = conn.cursor()
    cursor.execute("SELECT sqlite_version()")
    return cursor.fetchone()[0]