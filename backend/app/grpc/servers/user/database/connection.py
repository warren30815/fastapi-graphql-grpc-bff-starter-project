from .base import BaseDatabaseConnection
from .config import user_db_config

class UserDatabaseConnection(BaseDatabaseConnection):
    """User service database connection."""
    
    def __init__(self):
        super().__init__(user_db_config)

# Create instance
user_db = UserDatabaseConnection()

# Export commonly used objects
user_engine = user_db.engine
UserSessionLocal = user_db.SessionLocal
UserBase = user_db.Base
get_user_db_session = user_db.get_db_session
get_user_db = user_db.get_db