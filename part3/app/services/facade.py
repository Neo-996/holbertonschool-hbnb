#!/usr/bin/python3
"""Facade pattern implementation for HBnB services"""

from typing import Dict, Any, List, Optional
from .repositories.user_repository import UserRepository
from .repositories.place_repository import PlaceRepository
from .repositories.review_repository import ReviewRepository
from .repositories.amenity_repository import AmenityRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.users = UserRepository()
        self.places = PlaceRepository()
        self.reviews = ReviewRepository()
        self.amenities = AmenityRepository()

    # ----- USER METHODS -----
    def create_user(self, user_data: Dict[str, Any]) -> User:
        """Create new user with password hashing"""
        if self.users.get_user_by_email(user_data.get('email')):
            raise ValueError("Email already registered")

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        user.hash_password(user_data['password'])
        self.users.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.users.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.users.get_user_by_email(email)

    def get_all_users(self) -> List[User]:
        return self.users.get_all()

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[User]:
        user = self.users.get(user_id)
        if not user:
            return None
            
        if 'password' in user_data:
            user.hash_password(user_data.pop('password'))
            
        self.users.update(user_id, user_data)
        return user

    # ----- PLACE METHODS -----
    def create_place(self, place_data: Dict[str, Any]) -> Place:
        """Create new place with validation"""
        if not self.users.get(place_data["owner_id"]):
            raise ValueError("Owner not found")

        place = Place(**{
            k: v for k, v in place_data.items() 
            if k in [
                'title', 'description', 'price_per_night',
                'latitude', 'longitude', 'max_guests', 'owner_id'
            ]
        })
        
        self.places.add(place)
        return place

    def search_places(self, filters: Dict[str, Any]) -> List[Place]:
        """Advanced place search with filters"""
        query = self.places._session.query(Place)
        
        if 'min_price' in filters and 'max_price' in filters:
            query = query.filter(
                Place.price_per_night.between(
                    filters['min_price'] * 100,
                    filters['max_price'] * 100
                )
            )
            
        if 'owner_id' in filters:
            query = query.filter_by(owner_id=filters['owner_id'])
            
        return query.all()

    def get_place(self, place_id: str) -> Optional[Place]:
        return self.places.get(place_id)

    def get_places_by_owner(self, owner_id: str) -> List[Place]:
        return self.places.get_by_owner(owner_id)

    # ----- REVIEW METHODS -----
    def create_review(self, review_data: Dict[str, Any]) -> Review:
        """Create review with validation"""
        if not all(key in review_data for key in ['text', 'rating', 'user_id', 'place_id']):
            raise ValueError("Missing required fields")

        if not (1 <= review_data['rating'] <= 5):
            raise ValueError("Rating must be between 1-5")

        review = Review(**review_data)
        self.reviews.add(review)
        return review

    def get_place_reviews(self, place_id: str) -> List[Review]:
        return self.reviews.get_by_place(place_id)

    def get_place_rating(self, place_id: str) -> float:
        return self.reviews.get_average_rating(place_id) or 0.0

    # ----- AMENITY METHODS -----
    def create_amenity(self, name: str) -> Amenity:
        """Create new amenity with name validation"""
        if not name.strip():
            raise ValueError("Amenity name cannot be empty")
            
        amenity = Amenity(name=name)
        self.amenities.add(amenity)
        return amenity

    def find_amenities(self, search_term: str) -> List[Amenity]:
        return self.amenities.search_by_name(search_term)

    # ----- ADMIN METHODS -----
    def delete_entity(self, entity_type: str, entity_id: str) -> bool:
        """Generic delete method for admin"""
        repo = getattr(self, f"{entity_type}s", None)
        if not repo:
            raise ValueError("Invalid entity type")
            
        entity = repo.get(entity_id)
        if entity:
            repo.delete(entity_id)
            return True
        return False


# Singleton instance
facade = HBnBFacade()
