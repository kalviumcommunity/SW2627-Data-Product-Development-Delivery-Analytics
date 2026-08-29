"""
SQL Database Integration Demo Script
Demonstrates database setup and data loading for employee analytics.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.load_data import load_csv
from src.sql.db_integration import (
    create_connection,
    create_tables_from_dataframes,
    get_table_info,
    list_tables,
    get_database_stats,
    execute_query,
    get_sqlite_version
)


# Define the raw datasets
RAW_DATASETS = {
    "employee_master_raw.csv": "employees",
    "timesheets_raw.csv": "timesheets",
    "allocations_raw.csv": "allocations",
    "billing_raw.csv": "billing"
}


def main():
    data_dir = Path(__file__).parent.parent / "data" / "raw"
    db_dir = Path(__file__).parent.parent / "data"
    
    print("=" * 60)
    print("SQL DATABASE INTEGRATION")
    print("=" * 60)
    
    # Create in-memory database
    print("\n--- Database Setup ---")
    conn = create_connection()
    print(f"SQLite version: {get_sqlite_version(conn)}")
    
    # Load all datasets
    print("\n--- Loading Data ---")
    dataframes = {}
    for filename, table_name in RAW_DATASETS.items():
        file_path = data_dir / filename
        if file_path.exists():
            df = load_csv(str(file_path))
            dataframes[table_name] = df
            print(f"Loaded {table_name}: {len(df)} rows, {len(df.columns)} columns")
    
    # Create tables
    print("\n--- Creating Tables ---")
    tables = create_tables_from_dataframes(conn, dataframes)
    print(f"Created {len(tables)} tables")
    
    # Get table info
    print("\n--- Table Information ---")
    for table in tables:
        info = get_table_info(conn, table)
        print(f"  {info['table_name']}: {info['row_count']} rows, {len(info['columns'])} columns")
    
    # Get database statistics
    print("\n--- Database Statistics ---")
    stats = get_database_stats(conn)
    print(f"Total tables: {stats['total_tables']}")
    for table_name, table_info in stats['tables'].items():
        print(f"  {table_name}: {table_info['row_count']} rows")
    
    # Execute sample queries
    print("\n--- Sample Queries ---")
    
    # Query 1: Employee count by department
    query1 = """
    SELECT department, COUNT(*) as employee_count
    FROM employees
    GROUP BY department
    ORDER BY employee_count DESC
    LIMIT 5
    """
    print("\nTop 5 departments by employee count:")
    result1 = execute_query(conn, query1)
    print(result1.to_string(index=False))
    
    # Query 2: Timesheet summary
    query2 = """
    SELECT 
        employee_id,
        COUNT(*) as timesheet_count,
        SUM(hours_logged) as total_hours,
        AVG(hours_logged) as avg_hours
    FROM timesheets
    GROUP BY employee_id
    LIMIT 5
    """
    print("\nSample timesheet summary:")
    result2 = execute_query(conn, query2)
    print(result2.to_string(index=False))
    
    # Close connection
    conn.close()
    
    print(f"\n{'=' * 60}")
    print("DATABASE INTEGRATION COMPLETE")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()