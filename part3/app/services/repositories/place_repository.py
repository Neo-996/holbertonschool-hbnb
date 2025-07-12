#!/usr/bin/python3
"""PlaceRepository: Handles database operations for Place model"""

from app.models.place import Place
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from typing import List, Optional

class PlaceRepository(SQLAlchemyRepository):
    """Repository class for Place entity with custom queries"""
    
    def __init__(self):
        super().__init__(Place)

    def get_by_owner(self, owner_id: str) -> List[Place]:
        """Get all places owned by specific user"""
        return self._session.query(self._model)\
                   .filter_by(owner_id=owner_id)\
                   .all()

    def search_by_price_range(self, min_price: float, max_price: float) -> List[Place]:
        """Search places within price range (in dollars)"""
        min_cents = int(min_price * 100)
        max_cents = int(max_price * 100)
        
        return self._session.query(self._model)\
                   .filter(self._model.price_per_night.between(min_cents, max_cents))\
                   .all()

    def get_by_location(self, latitude: float, longitude: float, radius_km: float = 10) -> List[Place]:
        """Get places within radius of location (simplified)"""
        # Note: For production, use PostGIS or similar for real distance calculations
        return self._session.query(self._model)\
                   .filter(
                       (self._model.latitude.between(latitude - 0.1, latitude + 0.1)) &
                       (self._model.longitude.between(longitude - 0.1, longitude + 0.1))
                   )\
                   .all()
