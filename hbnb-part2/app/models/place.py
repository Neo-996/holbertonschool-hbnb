def __init__(self, title, description, price_per_night, latitude,
             longitude, max_guests, owner_id, amenities=None, id=None):
    super().__init__()

    if not title or len(title) > 100:
        raise ValueError("Invalid title")
    if price_per_night <= 0:
        raise ValueError("Price must be positive")
    if not (-90 <= latitude <= 90):
        raise ValueError("Invalid latitude")
    if not (-180 <= longitude <= 180):
        raise ValueError("Invalid longitude")
    if not owner_id:
        raise ValueError("Owner ID is required")

    self.id = id or self.id
    self.title = title
    self.description = description or ""
    self.price = price_per_night
    self.latitude = latitude
    self.longitude = longitude
    self.max_guests = max_guests
    self.owner = owner_id
    self.amenities = amenities or []
    self.reviews = []
