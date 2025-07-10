from typing import Dict, Any, List, Optional
from app.services.repositories.user_repository import UserRepository
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()  # specialized for User
        self.amenity_repo = SQLAlchemyRepository(Amenity)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # ----- USER METHODS -----
    def create_user(self, user_data: Dict[str, Any]) -> User:
        if self.user_repo.get_user_by_email(user_data.get('email')):
            raise ValueError("Email already registered")

        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        user.set_password(user_data['password'])  # Hash password before saving
        self.user_repo.add(user)
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self) -> List[User]:
        return self.user_repo.get_all()

    def update_user(self, user_id: str, user_data: Dict[str, Any]) -> Optional[User]:
        user = self.user_repo.get(user_id)
        if not user:
            return None
        if 'password' in user_data:
            user.set_password(user_data.pop('password'))
        self.user_repo.update(user_id, user_data)
        return user

    def delete_user(self, user_id: str) -> bool:
        if self.user_repo.get(user_id):
            self.user_repo.delete(user_id)
            return True
        return False

    # ----- AMENITY METHODS -----
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
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    def delete_amenity(self, amenity_id: str) -> bool:
        if self.get_amenity(amenity_id):
            self.amenity_repo.delete(amenity_id)
            return True
        return False

    # ----- PLACE METHODS -----
    def create_place(self, place_data: Dict[str, Any]) -> Place:
        owner = self.get_user(place_data["owner_id"])
        if not owner:
            raise ValueError("Owner not found")

        amenity_ids = place_data.pop("amenities", [])

        # Create Place instance — assuming your Place expects owner_id, not owner object
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ""),
            price_per_night=place_data['price_per_night'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            max_guests=place_data['max_guests'],
            owner_id=owner.id,
        )

        # Add amenities by loading Amenity objects
        for amenity_id in amenity_ids:
            amenity = self.get_amenity(amenity_id)
            if amenity:
                place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id: str) -> Optional[Place]:
        return self.place_repo.get(place_id)

    def get_all_places(self) -> List[Place]:
        return self.place_repo.get_all()

    def update_place(self, place_id: str, place_data: Dict[str, Any]) -> Optional[Place]:
        place = self.place_repo.get(place_id)
        if not place:
            return None
        self.place_repo.update(place_id, place_data)
        return place

    def delete_place(self, place_id: str) -> bool:
        if self.place_repo.get(place_id):
            self.place_repo.delete(place_id)
            return True
        return False

    # ----- REVIEW METHODS -----
    def create_review(self, review_data: Dict[str, Any]) -> Review:
        place = self.get_place(review_data["place_id"])
        user = self.get_user(review_data["user_id"])
        if not place or not user:
            raise ValueError("Invalid user or place")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=place.id,
            user_id=user.id
        )
        self.review_repo.add(review)
        return review

    def get_review(self, review_id: str) -> Optional[Review]:
        return self.review_repo.get(review_id)

    def get_all_reviews(self) -> List[Review]:
        return self.review_repo.get_all()

    def update_review(self, review_id: str, review_data: Dict[str, Any]) -> Optional[Review]:
        review = self.review_repo.get(review_id)
        if not review:
            return None
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id: str) -> bool:
        if self.review_repo.get(review_id):
            self.review_repo.delete(review_id)
            return True
        return False

    def user_reviewed_place(self, user_id: str, place_id: str) -> bool:
        reviews = self.review_repo.get_all()
        return any(r.user_id == user_id and r.place_id == place_id for r in reviews)


# Singleton facade instance
facade = HBnBFacade()

