#!/usr/bin/python3
"""UserRepository: Handles User-specific database operations"""

from app.models.user import User
from app.persistence.sqlalchemy_repository import SQLAlchemyRepository


class UserRepository(SQLAlchemyRepository):
    """Repository class for User entity, extends generic SQLAlchemyRepository"""

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str):
        """Retrieve a user by their email address"""
        return self.model.query.filter_by(email=email).first()

