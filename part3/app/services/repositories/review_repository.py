#!/usr/bin/python3
"""ReviewRepository: Handles database operations for Review model"""

from app.models.review import Review
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from typing import List, Optional

class ReviewRepository(SQLAlchemyRepository):
    """Repository class for Review entity with custom queries"""
    
    def __init__(self):
        super().__init__(Review)

    def get_by_place(self, place_id: str) -> List[Review]:
        """Get all reviews for a specific place"""
        return self._session.query(self._model)\
                   .filter_by(place_id=place_id)\
                   .order_by(self._model.created_at.desc())\
                   .all()

    def get_by_user(self, user_id: str) -> List[Review]:
        """Get all reviews by a specific user"""
        return self._session.query(self._model)\
                   .filter_by(user_id=user_id)\
                   .all()

    def get_average_rating(self, place_id: str) -> Optional[float]:
        """Calculate average rating for a place"""
        result = self._session.query(
                    db.func.avg(self._model.rating).label('average')
                 )\
                 .filter_by(place_id=place_id)\
                 .first()
        
        return result[0] if result[0] is not None else None
