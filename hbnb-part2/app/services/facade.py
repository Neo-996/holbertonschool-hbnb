from typing import Dict, Any, List, Optional
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # User methods
    def create_user(self, user_data: Dict[str, Any]) -> User:
        if self.get_user_by_email(user_data.get('email')):
            raise ValueError("Email already registered")
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self) -> List[User]:
        return self.user_repo.get_all()

    def list_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[User]:
        user = self.user_repo.get(user_id)
        if not user:
            return None
        for key, value in user_data.items():
            setattr(user, key, value)
        return user

    # Amenity methods
    def create_amenity(self, amenity_data: Dict[str, Any]) -> Amenity:
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id: str) -> Optional[Amenity]:
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self) -> List[Amenity]:
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id: str, amenity_data: Dict[str, Any]) -> Optional[Amenity]:
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # Place methods
    def create_place(self, place_data: Dict[str, Any]) -> Dict[str, Any]:
        price = place_data.get('price')
        lat = place_data.get('latitude')
        lon = place_data.get('longitude')

        if price is None or price < 0:
            raise ValueError("Invalid price")

        if lat is None or lat < -90 or lat > 90:
            raise ValueError("Invalid latitude")

        if lon is None or lon < -180 or lon > 180:
            raise ValueError("Invalid longitude")

        owner_id = place_data.pop('owner_id', None)
        if not owner_id:
            raise ValueError("Owner ID is required")
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.pop('amenities', [])
        place = Place(owner=owner, **place_data)

        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place.to_dict()

    def get_place(self, place_id: str) -> Optional[Dict[str, Any]]:
        place = self.place_repo.get(place_id)
        return place.to_dict() if place else None

    def get_all_places(self) -> List[Dict[str, Any]]:
        return [p.to_dict() for p in self.place_repo.get_all()]

    # Review methods
    def create_review(self, review_data: Dict[str, Any]) -> Dict[str, Any]:
        text = review_data.get('text')
        rating = review_data.get('rating')
        place_id = review_data.get('place_id')
        user_id = review_data.get('user_id')

        if not text:
            raise ValueError("Review text is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")

        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        review = Review(text=text, rating=rating, place=place, user=user)
        self.review_repo.add(review)
        place.add_review(review)
        return review.to_dict()

    def get_review(self, review_id: str) -> Optional[Dict[str, Any]]:
        review = self.review_repo.get(review_id)
        return review.to_dict() if review else None

    def get_all_reviews(self) -> List[Dict[str, Any]]:
        return [r.to_dict() for r in self.review_repo.get_all()]

    def get_reviews_by_place(self, place_id: str) -> List[Dict[str, Any]]:
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return [r.to_dict() for r in place.reviews]

    def update_review(self, review_id: str, review_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        review = self.review_repo.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            setattr(review, key, value)
        return review.to_dict()

    def delete_review(self, review_id: str) -> bool:
        review = self.review_repo.get(review_id)
        if not review:
            return False
        self.review_repo.delete(review_id)
        if review.place and review in review.place.reviews:
            review.place.reviews.remove(review)
        return True


# Singleton instance to be shared across the app
facade = HBnBFacade()
