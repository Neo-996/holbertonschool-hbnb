#!/usr/bin/python3
"""Base SQLAlchemy model for all application models"""

from app import db
from datetime import datetime
import uuid

class BaseModel(db.Model):
    """
    BaseModel class that includes common attributes and methods
    for all other models in the application.
    """

    __abstract__ = True  # Prevents SQLAlchemy from creating a table for this class

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save this instance to the database"""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete this instance from the database"""
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        """Convert instance to dictionary (safe for API responses)"""
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            '__class__': self.__class__.__name__
        }

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.id}>"

