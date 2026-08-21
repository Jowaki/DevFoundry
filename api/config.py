import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    """App configuration"""
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    OPENAI_MODEL: str = "gpt-4"  # or "gpt-3.5-turbo" for cheaper testing
    
    # Validation
    if not OPENAI_API_KEY:
        raise ValueError("❌ OPENAI_API_KEY not found in .env!")

settings = Settings()