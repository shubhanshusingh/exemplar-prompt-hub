import pytest
from sqlalchemy import text
from app.db.session import SessionLocal
from app.db.base_class import Base
from app.core.config import settings

def test_database_connection():
    """Test that we can connect to the database and execute a simple query."""
    try:
        db = SessionLocal()
        result = db.execute(text('SELECT 1'))
        assert result.scalar() == 1
        db.close()
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")

def test_database_tables_exist():
    """Test that all required database tables exist."""
    try:
        db = SessionLocal()
        # Check Prompts table
        result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'prompts')"))
        assert result.scalar() is True
        
        # Check Tags table
        result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'tags')"))
        assert result.scalar() is True
        
        # Check PromptVersions table
        result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'prompt_versions')"))
        assert result.scalar() is True
        
        # Check prompt_tags association table
        result = db.execute(text("SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = 'prompt_tags')"))
        assert result.scalar() is True
        
        db.close()
    except Exception as e:
        pytest.fail(f"Database table check failed: {e}")

def test_database_schema():
    """Test that the database schema matches our expectations."""
    try:
        db = SessionLocal()
        
        # Check Prompts table columns
        result = db.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'prompts'
        """))
        columns = {row[0]: row[1] for row in result}
        assert 'id' in columns
        assert 'name' in columns
        assert 'text' in columns
        assert 'description' in columns
        assert 'version' in columns
        assert 'meta' in columns
        assert 'created_at' in columns
        assert 'updated_at' in columns
        
        db.close()
    except Exception as e:
        pytest.fail(f"Database schema check failed: {e}") 