from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv

# Load .env file if present
load_dotenv()


class AppSettings(BaseSettings):
    """Application configuration loaded from environment variables.
    Ensures Firebase private key is handled with escaped newlines from .env files.
    """
    FIREBASE_PROJECT_ID: str = Field(..., description="Firebase GCP project ID")
    FIREBASE_CLIENT_EMAIL: str = Field(..., description="Service account client email")
    FIREBASE_PRIVATE_KEY: str = Field(..., description="Service account private key with escaped newlines (\\n)")
    FIREBASE_STORAGE_BUCKET: str = Field(..., description="Firebase Storage bucket name")
    FIREBASE_WEB_API_KEY: str = Field(..., description="Firebase web API key")
    FIREBASE_MESSAGING_SENDER_ID: str = Field(..., description="Firebase messaging sender id")
    FIREBASE_APP_ID: str = Field(..., description="Firebase app id")

    BACKEND_BASE_URL: str | None = Field(default=None, description="Optional base URL for backend, used in deep links")

    model_config = SettingsConfigDict(env_file=None, extra="ignore")

    # PUBLIC_INTERFACE
    def private_key_with_newlines(self) -> str:
        """Return the FIREBASE_PRIVATE_KEY with proper newline characters."""
        key = self.FIREBASE_PRIVATE_KEY
        # Handle both '\\n' sequences and Windows-style CRLF escaped sequences
        return key.replace("\\n", "\n").replace("\\r", "\r")


# PUBLIC_INTERFACE
@lru_cache(maxsize=1)
def get_settings() -> AppSettings:
    """Get cached application settings."""
    return AppSettings()
