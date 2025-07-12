#!/usr/bin/python3
"""Place model implementation with SQLAlchemy ORM"""

from app import db
from .base_model import BaseModel
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from app.models.association import place_amenities  

class Place(BaseModel):
    __tablename__ = 'places'

    title = Column(String(100), nullable=False)
    description = Column(String(1024))
    price_per_night = Column(Integer, nullable=False)  # Stored in cents
    latitude = Column(Float)
    longitude = Column(Float)
    max_guests = Column(Integer, nullable=False)
    owner_id = Column(String(60), ForeignKey('users.id'), nullable=False)

    
    reviews = db.relationship('Review', backref='place', cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenities, backref='places')

    def __init__(self, **kwargs):
        if 'price_per_night' in kwargs:
            try:
                kwargs['price_per_night'] = int(float(kwargs['price_per_night']) * 100)
            except (ValueError, TypeError):
                raise ValueError("Price must be a valid number")

        if 'title' not in kwargs or len(kwargs.get('title', '').strip()) < 1:
            raise ValueError("Title is required")

        super().__init__(**kwargs)

    @property
    def display_price(self):
        return self.price_per_night / 100

    def to_dict(self):
        data = super().to_dict()
        data.update({
            'title': self.title,
            'description': self.description,
            'price_per_night': self.display_price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'max_guests': self.max_guests,
            'owner_id': self.owner_id,
            '__class__': self.__class__.__name__
        })
        return data

    def __repr__(self):
        return f"<Place {self.id}: {self.title}>"
