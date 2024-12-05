import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL","postgresql://youruser:yourpassword@db:5432/yourdb")
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY","AIzaSyCeECOknuR_tIhqysYalCnO4TECzDYo9tw")
    GEMINI_MODEL =  'gemini-1.0-pro'
settings = Settings()
