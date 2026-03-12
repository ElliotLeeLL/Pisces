from loguru import logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from zenml.client import Client
from zenml.exceptions import EntityExistsError
 
class Settings(BaseSettings):
    # MongoDB database
    DATABASE_HOST: str = "mongodb://llm_engineering:llm_engineering@127.0.0.1:27017"
    DATABASE_NAME: str = "twin"

    # Qdrant vector database
    USE_QDRANT_CLOUD: bool = False
    QDRANT_DATABASE_HOST: str = "localhost"
    QDRANT_DATABASE_PORT: int = 6333
    QDRANT_CLOUD_URL: str = "str"
    QDRANT_APIKEY: str | None = None