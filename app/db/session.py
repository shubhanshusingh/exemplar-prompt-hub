from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL, connect_args={"check_same_thread": False}
    )
else:
    engine = create_engine(settings.DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text('SELECT 1'))
        print("Database connection successful!")
    except Exception as e:
        print(f"Database connection failed: {e}")
    finally:
        db.close()

# Call the test function
test_db_connection() 