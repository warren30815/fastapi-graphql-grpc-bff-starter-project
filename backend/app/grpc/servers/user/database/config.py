import os
from .base import BaseDatabaseConfig

class UserServiceDatabaseConfig(BaseDatabaseConfig):
    """User service database configuration settings."""

    def __init__(self):
        super().__init__("user")

    def _get_database_url(self) -> str:
        """Get database URL from environment variables."""
        # Check for full USER_DATABASE_URL first
        database_url = os.getenv("USER_DATABASE_URL")
        if database_url:
            return database_url

        # Build URL from individual components
        return self._build_url_from_components("USER")

user_db_config = UserServiceDatabaseConfig()
