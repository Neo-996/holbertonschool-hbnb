#!/usr/bin/python3
"""Place model implementation"""
from .base_model import BaseModel
from typing import List, Optional


class Place(BaseModel):
    """
    Place class represents a rental property listing.
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
        super().__init__()
        self.id = id or self.id
        self.title = title
        self.description = description
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
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Description must be a string")
        self._description = value

    @property
    def price_per_night(self) -> float:
        return self._price_per_night

    @price_per_night.setter
    def price_per_night(self, value: float):
        if not isinstance(value, (float, int)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price_per_night = float(value)

    @property
    def latitude(self) -> float:
        return self._latitude

    @latitude.setter
    def latitude(self, value: float):
        if not isinstance(value, (float, int)) or not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self) -> float:
        return self._longitude

    @longitude.setter
    def longitude(self, value: float):
        if not isinstance(value, (float, int)) or not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    @property
    def max_guests(self) -> int:
        return self._max_guests

    @max_guests.setter
    def max_guests(self, value: int):
        if not isinstance(value, int) or value < 1:
            raise ValueError("Max guests must be an integer >= 1")
        self._max_guests = value

    @property
    def owner_id(self) -> str:
        return self._owner_id

    @owner_id.setter
    def owner_id(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Owner ID must be a non-empty string")
        self._owner_id = value

    def add_amenity(self, amenity_id: str):
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)
            self.save()

    def add_review(self, review_id: str):
        if review_id not in self.reviews:
            self.reviews.append(review_id)
            self.save()

    def to_dict(self) -> dict:
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
            'reviews': self.reviews.copy(),
            '__class__': self.__class__.__name__
        })
        return data

    def __str__(self) -> str:
        return f"[Place] ({self.id}) {self.title} - ${self.price_per_night}/night"

