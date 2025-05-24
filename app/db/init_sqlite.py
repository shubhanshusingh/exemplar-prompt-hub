import sqlite3
import os
from pathlib import Path

def init_sqlite_db():
    # Get the directory of this file
    current_dir = Path(__file__).parent
    
    # Create database directory if it doesn't exist
    db_dir = current_dir / "sqlite"
    db_dir.mkdir(exist_ok=True)
    
    # Database file path
    db_path = db_dir / "prompts.db"
    
    # Read the schema file
    schema_path = current_dir / "sqlite_schema.sql"
    with open(schema_path, 'r') as f:
        schema = f.read()
    
    # Connect to SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(db_path)
    
    try:
        # Execute the schema
        conn.executescript(schema)
        conn.commit()
        print(f"Database initialized successfully at {db_path}")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    init_sqlite_db() 