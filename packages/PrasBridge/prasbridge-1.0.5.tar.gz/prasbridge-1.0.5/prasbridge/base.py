from sqlalchemy import Column, DateTime, func, Integer
from sqlalchemy.ext.declarative import declared_attr, declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from .mixins import UserMixin
from .serializers import PrasSerializer, IntegratedMeta
from datetime import datetime
from .session import SQLAlchemySessionManager


Base = declarative_base(metaclass=IntegratedMeta)

session_manager = SQLAlchemySessionManager()
session = session_manager.get_session()

class PrasBase(Base, PrasSerializer):
    """Base class for all models."""

    __abstract__ = True

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.now(), nullable=True)
    
    @declared_attr
    def id(cls):
        return Column(Integer, primary_key=True, autoincrement=True, nullable=True)
    
    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.now(), onupdate=datetime.now(), nullable=True)

    def save(self, session=session):
        """Custom save method to handle session operations."""
        session.add(self)
        session.commit()
        
            
    

class BaseUser(PrasBase, UserMixin):
    """Base user class that combines basic user fields and utility functions."""

    __abstract__ = True

    @declared_attr
    def username(cls):
        return Column(String(255), unique=True, nullable=False)
    
    @declared_attr
    def first_name(cls):
        return Column(String(30), nullable=True)
    
    @declared_attr
    def last_name(cls):
        return Column(String(30), nullable=True)
    
    @declared_attr
    def email(cls):
        return Column(String(255), unique=True, nullable=False)
    
    @declared_attr
    def password(cls):
        return Column(String(128), nullable=False) 
    
    @declared_attr
    def is_active(cls):
        return Column(Boolean, default=True)
    
    @declared_attr
    def is_staff(cls):
        return Column(Boolean, default=False)
    
    @declared_attr
    def is_superuser(cls):
        return Column(Boolean, default=False)
    
    @declared_attr
    def date_joined(cls):
        return Column(DateTime, default=func.now())

    def __repr__(self):
        return f"<BaseUser(username={self.username}, email={self.email})>"
