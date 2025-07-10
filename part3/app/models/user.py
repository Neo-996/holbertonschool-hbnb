#!/usr/bin/python3
"""User model implementation with SQLAlchemy ORM and password hashing"""

from app import db, bcrypt
from .base_model import BaseModel

class User(BaseModel):
    """
    User SQLAlchemy model representing application users.

    Attributes:
        first_name (str): User's first name
        last_name (str): User's last name
        email (str): Unique user email
        password (str): Hashed password
        is_admin (bool): Admin flag
    """

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def hash_password(self, plain_password):
        """Hash a plaintext password and store it"""
        if not plain_password or len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    def verify_password(self, plain_password):
        """Check if provided password matches hashed one"""
        return bcrypt.check_password_hash(self.password, plain_password)

    def to_dict(self):
        """Convert user instance to dictionary excluding sensitive data"""
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            '__class__': self.__class__.__name__
        })
        return data

    def __repr__(self):
        return f"<User {self.email}>"

