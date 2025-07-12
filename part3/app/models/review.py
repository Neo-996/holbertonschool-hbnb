#!/usr/bin/python3
"""Review model implementation with SQLAlchemy ORM"""

from app import db
from .base_model import BaseModel
from sqlalchemy import Column, String, Integer, ForeignKey, Text, CheckConstraint

class Review(BaseModel):
    """
    Review SQLAlchemy model representing user reviews.
    
    Attributes:
        text (str): Review content (1-1024 chars)
        rating (int): Rating (1-5 stars)
        place_id (str): Reference to Place
        user_id (str): Reference to User
    """
    __tablename__ = 'reviews'
    __table_args__ = (
        CheckConstraint('rating BETWEEN 1 AND 5', name='check_rating_range'),
    )

    # SQLAlchemy Columns
    text = Column(Text, nullable=False)
    rating = Column(Integer, nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs):
        """
        Initialize with validation:
        - Validates rating range
        - Validates text length
        """
        if 'rating' in kwargs and not (1 <= kwargs['rating'] <= 5):
            raise ValueError("Rating must be between 1-5")
            
        if 'text' in kwargs and len(kwargs['text'].strip()) < 1:
            raise ValueError("Review text cannot be empty")
            
        super().__init__(**kwargs)

    def to_dict(self):
        """Serialize to dictionary"""
        data = super().to_dict()
        data.update({
            'text': self.text,
            'rating': self.rating,
            'place_id': self.place_id,
            'user_id': self.user_id,
            '__class__': self.__class__.__name__
        })
        return data

    def __repr__(self):
        return f"<Review {self.id} (Rating: {self.rating}/5)>"
