"""
Environment Configuration Management
Centralized configuration for all environments
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )
    
    # API Keys
    groq_api_key: str
    
    # Database
    chroma_persist_dir: str = "./data/chroma"
    chroma_collection_name: str = "mutual_fund_chunks"
    
    # Phase 3 API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    cors_origins: str = "http://localhost:3000,http://localhost:8501"
    
    # Phase 4 UI
    streamlit_server_port: int = 8501
    streamlit_server_address: str = "0.0.0.0"
    
    # Phase 2 RAG
    embedding_model: str = "BAAI/bge-small-en-v1.5"
    chunk_size: int = 500
    chunk_overlap: int = 50
    max_retrieved_chunks: int = 5
    similarity_threshold: float = 0.7
    
    # Caching
    cache_enabled: bool = True
    cache_ttl: int = 3600
    
    # Logging
    log_level: str = "INFO"
    log_format: str = "json"
    
    # Environment
    environment: str = "development"
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse CORS origins string into list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    def get_cors_origins(self) -> list[str]:
        """Get CORS origins as list."""
        return self.cors_origins_list


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get settings instance."""
    return settings
