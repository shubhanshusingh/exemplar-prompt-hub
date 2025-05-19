from setuptools import setup, find_packages

setup(
    name="exemplar-prompt-hub",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.104.1",
        "uvicorn==0.24.0",
        "sqlalchemy==2.0.23",
        "pydantic==2.5.2",
        "python-multipart==0.0.6",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "alembic==1.12.1",
        "python-dotenv==1.0.0",
    ],
    python_requires=">=3.8",
) 