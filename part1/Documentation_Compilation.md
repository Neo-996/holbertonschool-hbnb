# HBnB Evolution – Technical Documentation

## 📘 Introduction
This document provides a comprehensive technical overview of the HBnB Evolution application.  
It compiles all major architecture diagrams and explanations developed throughout the project.  
The goal is to guide the implementation process by providing a clear reference for the application’s design and logic.

---

## 🗂️ High-Level Architecture

### High-Level Package Diagram
```mermaid
classDiagram
    class PresentationLayer {
        <<Interface>>
        +ServiceAPI
    }

    class BusinessLogicLayer {
        +User
        +Place
        +Review
        +Amenity
    }

    class PersistenceLayer {
        +DatabaseAccess
        +Repository
    }

    PresentationLayer --> BusinessLogicLayer : Facade Pattern
    BusinessLogicLayer --> PersistenceLayer : Database Operations
```

**Explanation:**
- The system is divided into three layers: Presentation, Business Logic, and Persistence.
- Each layer has a specific role and communicates with the others using defined patterns.
- The `Facade Pattern` simplifies the interface between the Presentation and Business Logic layers.
- The Business Logic Layer communicates with the Persistence Layer using repositories and database operations.

---

## 🧩 Business Logic Layer - Class Diagram
```mermaid
classDiagram
    class BaseModel {
        <<Abstract>>
        +id: UUID
        +created_at: DateTime
        +updated_at: DateTime
        +save(): void
        +delete(): void
        +to_dict(): Dict
    }

    class User {
        +first_name: String
        +last_name: String
        +email: String
        +password_hash: String
        +is_admin: Boolean
        +authenticate(password: String): Boolean
        +update_profile(updates: Dict): Boolean
        +change_password(old_pass: String, new_pass: String): Boolean
    }

    class Place {
        +title: String
        +description: String
        +price_per_night: Decimal
        +latitude: Float
        +longitude: Float
        +max_guests: Integer
        +calculate_total_price(nights: Integer): Decimal
        +get_average_rating(): Float
    }

    class Review {
        +rating: Integer (1-5)
        +comment: String
        +update_comment(new_comment: String): void
        +update_rating(new_rating: Integer): void
    }

    class Amenity {
        +name: String
        +description: String
        +icon: String
    }

    BaseModel <|-- User
    BaseModel <|-- Place
    BaseModel <|-- Review
    BaseModel <|-- Amenity

    User "1" -- "0..*" Place : owns
    User "1" -- "0..*" Review : writes
    Place "1" -- "0..*" Review : has
    Place "0..*" -- "0..*" Amenity : has
```

**Explanation:**
- All entities inherit from `BaseModel`, which provides ID and timestamps.
- `User` owns `Place` and writes `Review`.
- `Place` has many `Review`s and `Amenity` objects.

---

## 🔁 Sequence Diagrams for API Calls

### 1. User Registration
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Register User (first name, last name, email, password)
    API->>BusinessLogic: Validate and Create User
    BusinessLogic->>Database: Insert User Data
    Database-->>BusinessLogic: Success/Failure
    BusinessLogic-->>API: Return Response
    API-->>User: Registration Successful/Error
```

### 2. Place Creation
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Create Place (title, description, price, location)
    API->>BusinessLogic: Validate and Create Place
    BusinessLogic->>Database: Insert Place Data
    Database-->>BusinessLogic: Success/Failure
    BusinessLogic-->>API: Return Response
    API-->>User: Place Created Successfully/Error
```

### 3. Review Submission
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Submit Review (place ID, rating, comment)
    API->>BusinessLogic: Validate and Create Review
    BusinessLogic->>Database: Insert Review Data
    Database-->>BusinessLogic: Success/Failure
    BusinessLogic-->>API: Return Response
    API-->>User: Review Submitted Successfully/Error
```

### 4. Fetching a List of Places
```mermaid
sequenceDiagram
    participant User
    participant API
    participant BusinessLogic
    participant Database

    User->>API: Request List of Places (filters: location, price, amenities)
    API->>BusinessLogic: Process Request and Apply Filters
    BusinessLogic->>Database: Fetch Filtered Places
    Database-->>BusinessLogic: Return List of Places
    BusinessLogic-->>API: Return Places Data
    API-->>User: Display List of Places
```

---

## ✅ Conclusion
This document compiles all architectural, design, and interaction diagrams for the HBnB Evolution project.  
It serves as a solid reference for implementation, testing, and future maintenance.  
Using a layered structure, clear object-oriented models, and sequence diagrams, this blueprint ensures a maintainable and scalable application.

