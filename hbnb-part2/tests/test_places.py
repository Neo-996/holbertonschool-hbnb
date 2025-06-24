import unittest
from app import create_app

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_place(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Sea View Apartment",
            "description": "Nice view",
            "price_per_night": 150.0,
            "latitude": 24.7,
            "longitude": 46.6,
            "max_guests": 3,
            "owner_id": "owner-123",
            "amenities": []
        })
        self.assertEqual(response.status_code, 201)

    def test_create_place_invalid_price(self):
        response = self.client.post('/api/v1/places/', json={
            "title": "Invalid Place",
            "description": "Bad input",
            "price_per_night": -20,
            "latitude": 24.7,
            "longitude": 46.6,
            "max_guests": 3,
            "owner_id": "owner-123",
            "amenities": []
        })
        self.assertEqual(response.status_code, 400)
