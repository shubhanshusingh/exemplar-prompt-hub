from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.endpoints import prompts
from app.db.base_class import Base
from app.db.session import engine
import uvicorn

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    prompts.router,
    prefix=f"{settings.API_V1_STR}/prompts",
    tags=["prompts"]
)

@app.get("/")
def read_root():
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

def main():
    """Run the FastAPI application using uvicorn."""
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG
    )

if __name__ == "__main__":
    main() 