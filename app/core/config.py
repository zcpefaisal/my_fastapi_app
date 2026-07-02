from pydantic_settings import BaseSettings,SettingsConfigDict
from pydantic import computed_field

class Settings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DB: str

    # Using computed_field to dynamically create DATABASE_URL
    @computed_field
    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Describe to Pydantic where the .env file is located
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

# Creating a global object, which will be imported and used throughout the project
settings = Settings()