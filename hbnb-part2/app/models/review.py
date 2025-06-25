#!/usr/bin/python3
"""Review model implementation"""
from .base_model import BaseModel
from typing import Dict, Any

class Review(BaseModel):
    """
    Review class represents a user's review of a place.
    
    Attributes:
        text (str): Review content (1-1024 chars)
        rating (int): Rating (1-5 stars)
        place_id (str): Associated place ID
        user_id (str): Reviewing user ID
    """
    
    def __init__(
        self,
        text: str,
        rating: int,
        place_id: str,
        user_id: str
    ):
        """
        Initialize a Review instance with validated attributes.
        
        Args:
            text: Review content
            rating: Star rating (1-5)
            place_id: ID of reviewed place
            user_id: ID of reviewing user
            
        Raises:
            ValueError: For invalid attribute values
        """
        super().__init__()
        
        # Use property setters for validation
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @property
    def text(self) -> str:
        """Get review text"""
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        """Set review text with validation"""
        if not isinstance(value, str) or not 1 <= len(value) <= 1024:
            raise ValueError("Review text must be 1-1024 characters")
        self._text = value

    @property
    def rating(self) -> int:
        """Get review rating"""
        return self._rating

    @rating.setter
    def rating(self, value: int) -> None:
        """Set review rating with validation"""
        if not isinstance(value, int) or not 1 <= value <= 5:
            raise ValueError("Rating must be integer between 1-5")
        self._rating = value

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert review to dictionary representation.
        
        Returns:
            Dictionary containing all review attributes
        """
        data = super().to_dict()
        data.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            '__class__': self.__class__.__name__
        })
        return data

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update review attributes from dictionary.
        
        Args:
            data: Dictionary of attributes to update
            
        Raises:
            ValueError: If data contains invalid attributes or values
        """
        for key, value in data.items():
            if not hasattr(self, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(self, key, value)
        self.save()

    def __str__(self) -> str:
        """String representation of the review"""
        return f"[Review] ({self.id}) {self.text[:50]}... (Rating: {self.rating})"
