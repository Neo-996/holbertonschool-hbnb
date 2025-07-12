#!/usr/bin/python3
"""AmenityRepository: Handles database operations for Amenity model"""

from app.models.amenity import Amenity
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository
from typing import List, Optional

class AmenityRepository(SQLAlchemyRepository):
    """Repository class for Amenity entity with custom queries"""
    
    def __init__(self):
        super().__init__(Amenity)

    def get_by_name(self, name: str) -> Optional[Amenity]:
        """Get amenity by exact name match"""
        return self._session.query(self._model)\
                   .filter_by(name=name)\
                   .first()

    def search_by_name(self, search_term: str) -> List[Amenity]:
        """Search amenities by name (case-insensitive partial match)"""
        return self._session.query(self._model)\
                   .filter(self._model.name.ilike(f"%{search_term}%"))\
                   .all()
