#!/usr/bin/python3
"""User model implementation with enhanced validation and documentation"""
import re
from typing import Dict, Any, Set
from .base_model import BaseModel

class User(BaseModel):
    """
    User class representing application users with admin capabilities.
    
    Class Attributes:
        _emails (Set[str]): Tracks all registered emails for uniqueness
    """
    
    _emails: Set[str] = set()  # Class-level email registry

    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        is_admin: bool = False
    ):
        """
        Initialize a User instance with validated attributes.
        
        Args:
            first_name: User's first name (1-50 chars)
            last_name: User's last name (1-50 chars)
            email: Valid and unique email address
            is_admin: Admin privileges flag
            
        Raises:
            ValueError: For invalid attribute values
        """
        super().__init__()
        
        # Use property setters for validation
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self._password = None  # Will be used for authentication

        User._emails.add(email)

    @property
    def first_name(self) -> str:
        """Get user's first name"""
        return self._first_name

    @first_name.setter
    def first_name(self, value: str) -> None:
        """Set first name with validation"""
        if not isinstance(value, str) or not 1 <= len(value) <= 50:
            raise ValueError("First name must be 1-50 characters")
        self._first_name = value

    @property
    def last_name(self) -> str:
        """Get user's last name"""
        return self._last_name

    @last_name.setter
    def last_name(self, value: str) -> None:
        """Set last name with validation"""
        if not isinstance(value, str) or not 1 <= len(value) <= 50:
            raise ValueError("Last name must be 1-50 characters")
        self._last_name = value

    @property
    def email(self) -> str:
        """Get user's email"""
        return self._email

    @email.setter
    def email(self, value: str) -> None:
        """Set email with format validation and uniqueness check"""
        if not isinstance(value, str):
            raise ValueError("Email must be a string")
            
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
            raise ValueError("Invalid email format")
            
        if value in User._emails and getattr(self, '_email', None) != value:
            raise ValueError("Email already registered")
            
        self._email = value

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert user to dictionary representation, excluding sensitive data.
        
        Returns:
            Dictionary containing safe user attributes
        """
        data = super().to_dict()
        data.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            '__class__': self.__class__.__name__
        })
        return data

    def update(self, data: Dict[str, Any]) -> None:
        """
        Update user attributes from dictionary.
        
        Args:
            data: Dictionary of attributes to update
            
        Raises:
            ValueError: For invalid attributes or values
        """
        for key, value in data.items():
            if not hasattr(self, key):
                raise ValueError(f"Invalid attribute: {key}")
            if key == 'email' and value != self.email:
                raise ValueError("Email cannot be changed")
            setattr(self, key, value)
        self.save()

    def set_password(self, password: str) -> None:
        """Securely set user password"""
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters")
        
        self._password = password

    def verify_password(self, password: str) -> bool:
        """Verify user password"""
        return self._password == password

    def __str__(self) -> str:
        """String representation of the user"""
        return f"[User] {self.first_name} {self.last_name} <{self.email}>"
