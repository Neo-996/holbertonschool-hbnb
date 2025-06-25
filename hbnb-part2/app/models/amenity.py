#!/usr/bin/python3
"""Amenity model implementation"""
from .base_model import BaseModel

class Amenity(BaseModel):
    """
    Amenity class represents a facility or service offered by a place.
    
    Attributes:
        name (str): The name of the amenity (1-50 characters)
    """
    
    def __init__(self, name: str):
        """
        Initialize a new Amenity instance.
        
        Args:
            name (str): The name of the amenity
            
        Raises:
            ValueError: If name is invalid
        """
        super().__init__()
        self.name = name  # Uses property setter for validation

    @property
    def name(self) -> str:
        """Get the amenity name"""
        return self._name

    @name.setter
    def name(self, value: str):
        """Set the amenity name with validation"""
        if not isinstance(value, str) or not 1 <= len(value) <= 50:
            raise ValueError("Amenity name must be a string between 1-50 characters")
        self._name = value

    def __str__(self) -> str:
        """String representation of Amenity"""
        return f"[Amenity] ({self.id}) {self.__dict__}"
