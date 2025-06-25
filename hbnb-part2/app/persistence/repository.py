#!/usr/bin/python3
"""In-memory repository implementation for HBnB project"""
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        """Add new object with validation"""
        pass

    @abstractmethod
    def get(self, obj_id):
        """Get object by ID"""
        pass

    @abstractmethod
    def get_all(self):
        """Get all objects"""
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """Update object data"""
        pass

    @abstractmethod
    def delete(self, obj_id):
        """Delete object by ID"""
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """Find object by attribute"""
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        if not hasattr(obj, 'id'):
            raise ValueError("Object must have 'id' attribute")
        if obj.id in self._storage:
            raise ValueError(f"Object {obj.id} already exists")
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj and hasattr(obj, 'update'):
            obj.update(data)
            return True
        return False

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name, None) == attr_value),
            None
        )

    def __contains__(self, obj_id):
        """Support 'in' operator checking"""
        return obj_id in self._storage
