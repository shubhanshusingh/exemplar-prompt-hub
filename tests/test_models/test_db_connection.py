from app.db.session import SessionLocal
from sqlalchemy import text
import pytest

def test_database_connection():
    try:
        db = SessionLocal()
        db.execute(text('SELECT 1'))
        db.close()
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}") 