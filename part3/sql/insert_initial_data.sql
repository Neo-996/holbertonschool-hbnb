-- Insert admin user with timestamps
INSERT INTO users (
    id, first_name, last_name, email, password, is_admin, created_at, updated_at
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$5G7TQThqNgdbHqgZ71yaieHPZ5EvRU3taXZaX2AZK4VKvIkcGh07a',  
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert amenities with dynamic UUIDs and timestamps
INSERT INTO amenities (id, name, created_at, updated_at) VALUES
(UUID(), 'WiFi', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(UUID(), 'Swimming Pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
(UUID(), 'Air Conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
