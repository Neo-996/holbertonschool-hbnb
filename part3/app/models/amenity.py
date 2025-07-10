#!/usr/bin/python3
"""Amenity model implementation with SQLAlchemy"""

from .base_model import BaseModel
from app import db
import sqlalchemy as sa

class Amenity(BaseModel):
    """Amenity represents a facility or service offered by a place."""

    __tablename__ = 'amenities'

    # SQLAlchemy column for name
    _name = sa.Column("name", sa.String(50), nullable=False)

    def __init__(self, name: str):
        super().__init__()
        self.name = name  # Use setter for validation

    @property
    def name(self) -> str:
        """Get the amenity name."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the amenity name with validation."""
        if not isinstance(value, str) or not (1 <= len(value) <= 50):
            raise ValueError("Amenity name must be a string between 1 and 50 characters")
        self._name = value

    def __str__(self) -> str:
        """String representation of Amenity."""
        return f"[Amenity] ({self.id}) {self.name}"

