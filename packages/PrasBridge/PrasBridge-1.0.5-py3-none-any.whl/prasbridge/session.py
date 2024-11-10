from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from django.conf import settings
from contextlib import contextmanager

class SQLAlchemySessionManager:
    """Class to manage session operations."""
    
    def __init__(self):
        self.db_url = settings.DATABASES['sqlalchemy']['URL']
        self.engine = None
        self.Session = None

        if self.db_url is None:
            raise RuntimeError("Database URL is not set in settings.py.")
    
    def _initialize_engine(self):
        """Initialize the SQLAlchemy engine and session."""
        if self.engine is None:
            try:
                self.engine = create_engine(self.db_url, pool_pre_ping=True)
                self.Session = sessionmaker(bind=self.engine)
            except Exception as e:
                raise RuntimeError(f"Error initializing the database engine: {e}")
    
    def get_session(self):
        """Get a new session. Ensure the engine is initialized."""
        self._initialize_engine()
        return self.Session()
    
    def close(self, session):
        """Close the provided session."""
        if session:
            session.close()

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope for session management."""
        session = self.get_session()
        try:
            yield session
            session.commit()
            session.flush()
        except Exception as e:
            session.rollback()
            raise
        finally:
            self.close(session)
