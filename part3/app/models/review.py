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
        """
        super().__init__()
        self.text = text
        self.rating = rating
        self.place_id = place_id
        self.user_id = user_id

    @property
    def text(self) -> str:
        return self._text

    @text.setter
    def text(self, value: str) -> None:
        if not isinstance(value, str) or not 1 <= len(value) <= 1024:
            raise ValueError("Review text must be 1-1024 characters")
        self._text = value

    @property
    def rating(self) -> int:
        return self._rating

    @rating.setter
    def rating(self, value: int) -> None:
        if not isinstance(value, int) or not 1 <= value <= 5:
            raise ValueError("Rating must be integer between 1-5")
        self._rating = value

    @property
    def place_id(self) -> str:
        return self._place_id

    @place_id.setter
    def place_id(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("place_id must be a non-empty string")
        self._place_id = value

    @property
    def user_id(self) -> str:
        return self._user_id

    @user_id.setter
    def user_id(self, value: str) -> None:
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("user_id must be a non-empty string")
        self._user_id = value

    def to_dict(self) -> Dict[str, Any]:
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
        for key, value in data.items():
            if not hasattr(self, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(self, key, value)
        self.save()

    def __str__(self) -> str:
        return f"[Review] ({self.id}) {self.text[:50]}... (Rating: {self.rating})"

