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
    
    # Environment (development, staging, production)
    ENVIRONMENT: str = "development"
    
    @field_validator("ENVIRONMENT", mode="after")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment is one of allowed values"""
        allowed = ["development", "staging", "production"]
        if v not in allowed:
            raise ValueError(
                f"ENVIRONMENT must be one of {allowed}. Got: {v}"
            )
        return v
    
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "College ERP API"
    
    # Database
    DATABASE_URL: str

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def fix_database_url(cls, v: str) -> str:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
    @classmethod
    def fix_database_url(cls, v: str) -> str:
        if v and v.startswith("postgres://"):
            return v.replace("postgres://", "postgresql://", 1)
        return v
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Security
    SECRET_KEY: str = ""
    
    @field_validator("SECRET_KEY", mode="after")
    @classmethod
    def validate_secret_key(cls, v: str) -> str:
        """Validate SECRET_KEY is set and secure"""
        if not v:
            raise ValueError(
                "SECRET_KEY must be set. Generate with: "
                "python -c 'import secrets; print(secrets.token_urlsafe(32))'"
            )
        
        # In production, enforce minimum length
        import os
        if os.getenv("ENVIRONMENT") == "production":
            if len(v) < 32:
                raise ValueError(
                    "SECRET_KEY must be at least 32 characters in production"
                )
        
        return v
    
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Backend Base URL (for payment callbacks, etc.)
    BACKEND_BASE_URL: str = ""
    
    @field_validator("BACKEND_BASE_URL", mode="after")
    @classmethod
    def validate_backend_url(cls, v: str) -> str:
        """Validate BACKEND_BASE_URL is set and uses HTTPS in production"""
        if not v:
            raise ValueError("BACKEND_BASE_URL must be set")
        
        # In production, enforce HTTPS
        import os
        if os.getenv("ENVIRONMENT") == "production":
            if not v.startswith("https://"):
                raise ValueError(
                    f"BACKEND_BASE_URL must use HTTPS in production. Got: {v}"
                )
        
        return v
    
    # Portal Base URL (for email links)
    PORTAL_BASE_URL: str = ""
    
    @field_validator("PORTAL_BASE_URL", mode="after")
    @classmethod
    def validate_portal_url(cls, v: str) -> str:
        """Validate PORTAL_BASE_URL is set and uses HTTPS in production"""
        if not v:
            raise ValueError("PORTAL_BASE_URL must be set")
        
        # In production, enforce HTTPS
        import os
        if os.getenv("ENVIRONMENT") == "production":
            if not v.startswith("https://"):
                raise ValueError(
                    f"PORTAL_BASE_URL must use HTTPS in production. Got: {v}"
                )
        
        return v
    
    # CORS - Union[List[str], str] to handle both pre-parsed list and string
    BACKEND_CORS_ORIGINS: Union[List[str], str] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[str]:
        if isinstance(v, str):
            if not v or v.strip() == "":
                # Default for development
                return [
                    "http://localhost:3000",
                    "http://localhost:3001",
                    "http://localhost:8080",
                ]
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
    
    @field_validator("BACKEND_CORS_ORIGINS", mode="after")
    @classmethod
    def validate_cors_origins(cls, v: List[str]) -> List[str]:
        """Validate CORS origins include HTTPS in production"""
        import os
        if os.getenv("ENVIRONMENT") == "production":
            # Ensure at least one HTTPS origin in production
            # Check if any origin in the list starts with https://
            has_https = any(
                isinstance(origin, str) and origin.startswith("https://") 
                for origin in v
            )
            if not has_https:
                raise ValueError(
                    f"Production CORS must include at least one HTTPS origin. Got: {v}"
                )
        return v
    
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
    
    # Payment Gateway (Easebuzz)
    EASEBUZZ_MERCHANT_KEY: str = ""
    EASEBUZZ_SALT: str = ""
    EASEBUZZ_ENV: str = "test"  # test or prod

settings = Settings()

