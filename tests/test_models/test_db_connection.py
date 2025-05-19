from app.db.session import SessionLocal
import pytest

def test_database_connection():
    try:
        db = SessionLocal()
        db.execute('SELECT 1')
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")
    finally:
        db.close() 