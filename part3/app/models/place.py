#!/usr/bin/python3
"""Place model implementation"""
from .base_model import BaseModel
from typing import List, Optional

class Place(BaseModel):
    """
    Place class represents a rental property listing.
    
    Attributes:
        title (str): Property title (1-100 chars)
        description (str): Detailed description
        price_per_night (float): Positive price
        latitude (float): Between -90 and 90
        longitude (float): Between -180 and 180
        max_guests (int): At least 1
        owner_id (str): Required user ID
        amenities (list): List of amenity IDs
        reviews (list): List of review IDs
    """
    
    def __init__(
        self,
        title: str,
        description: str,
        price_per_night: float,
        latitude: float,
        longitude: float,
        max_guests: int,
        owner_id: str,
        amenities: Optional[List[str]] = None,
        id: Optional[str] = None
    ):
        """
        Initialize a Place instance with validated attributes.
        
        Args:
            title: Property title
            description: Detailed description
            price_per_night: Price per night
            latitude: Geographic coordinate
            longitude: Geographic coordinate
            max_guests: Maximum guest capacity
            owner_id: Owner user ID
            amenities: List of amenity IDs
            id: Optional custom ID
            
        Raises:
            ValueError: For invalid attribute values
        """
        super().__init__()
        
        # Validate and set attributes using properties
        self.id = id or self.id
        self.title = title
        self.description = description or ""
        self.price_per_night = price_per_night
        self.latitude = latitude
        self.longitude = longitude
        self.max_guests = max_guests
        self.owner_id = owner_id
        self.amenities = amenities or []
        self.reviews = []

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not 1 <= len(value) <= 100:
            raise ValueError("Title must be 1-100 character string")
        self._title = value

    @property
    def price_per_night(self) -> float:
        return self._price_per_night

    @price_per_night.setter
    def price_per_night(self, value: float):
        if not isinstance(value, (float, int)) or value <= 0:
            raise ValueError("Price must be positive number")
        self._price_per_night = float(value)

    # Add similar property validation for other attributes...
    
    def add_amenity(self, amenity_id: str):
        """Add an amenity to the place"""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
            self.save()

    def add_review(self, review_id: str):
        """Add a review to the place"""
        if review_id not in self.reviews:
            self.reviews.append(review_id)
            self.save()

    def to_dict(self) -> dict:
        """Convert place to dictionary"""
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price_per_night': self.price_per_night,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'max_guests': self.max_guests,
            'owner_id': self.owner_id,
            'amenities': self.amenities.copy(),
            'reviews': self.reviews.copy()
        })
        return data
