from pydantic_settings import BaseSettings
from typing import List, Optional
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Refaccionaria ERP"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # MySQL
    MYSQL_SERVER: str = "localhost"
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = ""
    MYSQL_DB: str = "refaccionaria_db"
    MYSQL_PORT: int = 3306
    
    # JWT
    SECRET_KEY: str = "clave-secreta-temporal-cambiar-en-produccion"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Aplicación
    LOCAL_ID: int = 1
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    @property
    def DATABASE_URL(self) -> str:
        # Permitir sobrescribir la URL de la base de datos mediante la variable de entorno DATABASE_URL
        env_db = os.getenv("DATABASE_URL")
        if env_db:
            return env_db
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()