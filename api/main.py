from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routers import auth
from api.database import engine
from api.models import Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Post Generator API",
    description="API для системы генерации постов с аутентификацией",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "http://frontend:3000",   # Docker network
        "http://127.0.0.1:3000",  # Alternative localhost
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["authentication"])

@app.get("/")
async def root():
    return {"message": "Post Generator API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
