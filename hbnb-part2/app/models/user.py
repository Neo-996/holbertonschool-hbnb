#!/usr/bin/python3

import re
from .base_model import BaseModel


class User(BaseModel):
    _emails = set()  # Simulate unique email check

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("Invalid first name")

        if not last_name or len(last_name) > 50:
            raise ValueError("Invalid last name")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        if email in User._emails:
            raise ValueError("Email must be unique")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        User._emails.add(email)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key) and key != "email":
                setattr(self, key, value)
        self.save()
