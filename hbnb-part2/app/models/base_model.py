#!/usr/bin/python3
"""Base model for all application models"""
import uuid
from datetime import datetime
from typing import Dict, Any

class BaseModel:
    """
    Base class that defines common attributes/methods for other models
    
    Attributes:
        id (str): Unique identifier
        created_at (datetime): Creation timestamp
        updated_at (datetime): Last update timestamp
    """
    
    def __init__(self):
        """Initialize base model with default values"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at

    def save(self) -> None:
        """Update the updated_at timestamp to current time"""
        self.updated_at = datetime.now()

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update model attributes from dictionary
        
        Args:
            data: Dictionary of attributes to update
            
        Raises:
            ValueError: If data contains invalid attributes
        """
        for key, value in data.items():
            if not hasattr(self, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(self, key, value)
        self.save()

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert model to dictionary representation
        
        Returns:
            Dictionary containing all model attributes
        """
        return {
            'id': self.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            '__class__': self.__class__.__name__
        }

    def __str__(self) -> str:
        """String representation of the model"""
        return f"[{self.__class__.__name__}] ({self.id}) {self.__dict__}"
