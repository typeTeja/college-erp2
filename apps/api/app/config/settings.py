from typing import Any, List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow"  # Allow extra fields from .env
    )
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "College ERP API"
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str = "default_secret_key_CHANGE_IN_PROD"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS - Union[List[str], str] to handle both pre-parsed list and string
    BACKEND_CORS_ORIGINS: Union[List[str], str] = [
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:8080",
    ]

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            if not v or v.strip() == "":
                return []
            if v.startswith("[") and v.endswith("]"):
                 import json
                 try:
                     return json.loads(v)
                 except:
                     pass
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list):
            return v
        return []
    
    # Storage Configuration (S3/MinIO)
    STORAGE_BACKEND: str = "s3"  # 's3' or 'local'
    S3_ENDPOINT: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_REGION: str = "us-east-1"
    S3_BUCKET: str = "college-erp-documents"  # Main documents bucket
    S3_BUCKET_IMAGES: str = "college-erp-images"  # Images bucket
    S3_BUCKET_TEMP: str = "college-erp-temp"  # Temporary files bucket
    S3_FORCE_PATH_STYLE: bool = True  # Required for MinIO
    CDN_BASE_URL: str = ""  # Optional CDN URL
    MAX_UPLOAD_SIZE: int = 10485760  # 10MB in bytes

settings = Settings()
