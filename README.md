# HBnB - UML
## Business Logic Layer

This layer manages the core entities and business rules of the HBnB app.

### Key Entities

- **User**: Represents a user of the platform. Ensures unique email addresses.
- **Place**: Listings owned by users. Supports latitude/longitude validation and has reviews and amenities.
- **Review**: Comments left by users for places. Supports rating (1–5).
- **Amenity**: Features associated with places (e.g., Wi-Fi, Parking).

### Relationships

- `User` → `Place`: One-to-many
- `Place` → `Review`: One-to-many
- `Place` ↔ `Amenity`: Many-to-many

### Example Usage

```python
user = User("Jane", "Doe", "jane@example.com")
place = Place("Sunny Villa", "Sea view", 200.0, 30.0, -70.0, user)
wifi = Amenity("Wi-Fi")
place.add_amenity(wifi)
review = Review("Loved it!", 5, place, user)
