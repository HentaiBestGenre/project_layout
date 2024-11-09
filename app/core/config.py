from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os


dotenv_path = os.path.join(os.path.dirname(__file__), '../../.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


class Settings(BaseSettings):
    HOST: str = os.getenv("HOST", "localhost")
    PORT: int = os.getenv("PORT", 8000)

settings = Settings()
