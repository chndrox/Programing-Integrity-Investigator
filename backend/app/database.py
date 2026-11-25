from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pydantic_settings import BaseSettings
from pydantic import Field
import os
from pathlib import Path

# Get the backend directory (where this file is located)
BASE_DIR = Path(__file__).parent.parent

class Settings(BaseSettings):
    database_url: str = Field(default="sqlite:///./pii.db")
    secret_key: str = Field(default="your-secret-key")
    algorithm: str = Field(default="HS256")
    access_token_expire_minutes: int = Field(default=30)
    groq_api_key: str = Field(default="")
    groq_model: str = Field(default="mixtral-8x7b-32768")
    max_file_size: int = Field(default=10485760)
    upload_dir: str = Field(default="./uploads")
    agent_concurrency_limit: int = Field(default=2)
    agent_timeout_seconds: int = Field(default=120)
    use_mock_mcp: bool = Field(default=True)

    class Config:
        env_file = str(BASE_DIR / ".env")
        case_sensitive = False

# Try to load settings from .env if it exists
try:
    settings = Settings()
except Exception as e:
    # If .env doesn't exist or has issues, use defaults
    print(f"Note: .env file not found or error loading it ({e}). Using default settings.")
    settings = Settings()

# Create database
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if "sqlite" in settings.database_url else {}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
