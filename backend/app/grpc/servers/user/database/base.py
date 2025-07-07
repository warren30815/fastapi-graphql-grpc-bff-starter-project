import os
from abc import ABC, abstractmethod
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

class BaseDatabaseConfig(ABC):
    """Base database configuration class."""

    def __init__(self, service_name: str):
        self.service_name = service_name
        self.database_url = self._get_database_url()

    @abstractmethod
    def _get_database_url(self) -> str:
        """Get database URL from environment variables."""
        pass

    def _build_url_from_components(self, service_prefix: str) -> str:
        """Build URL from individual environment variable components."""
        user = os.getenv(f"{service_prefix}_DB_USER", "postgres")
        password = os.getenv(f"{service_prefix}_DB_PASSWORD", "password")
        host = os.getenv(f"{service_prefix}_DB_HOST", "localhost")
        port = os.getenv(f"{service_prefix}_DB_PORT", "5432")
        database = os.getenv(f"{service_prefix}_DB_NAME", f"{self.service_name}_service")

        return f"postgresql://{user}:{password}@{host}:{port}/{database}"

class BaseDatabaseConnection:
    """Base database connection class."""

    def __init__(self, config: BaseDatabaseConfig):
        self.config = config
        self.engine = create_engine(
            config.database_url,
            pool_size=10  # Connection pool size
        )
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        self.Base = declarative_base()

    @contextmanager
    def get_db_session(self):
        """Context manager for database sessions."""
        db = self.SessionLocal()
        try:
            yield db
            db.commit()
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

    def get_db(self):
        """Dependency for FastAPI to get database session."""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
