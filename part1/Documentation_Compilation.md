# HBnB Evolution – Technical Documentation

## 📘 Introduction

This document serves as the complete technical blueprint for the **HBnB Evolution** application. It consolidates the high-level architectural design, core data models, and API interaction flows using standardized UML diagrams. The goal is to provide clear and actionable documentation that guides implementation and future scaling.

---

## 📂 High-Level Architecture

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

* **Presentation Layer** handles user requests via a unified API interface.
* **Business Logic Layer** contains all domain models and core services.
* **Persistence Layer** communicates with the database to perform all CRUD operations.
* The layers follow a **Facade Pattern** for simplicity and separation of concerns.

---

## 🧩 Business Logic Layer – Class Diagram

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

* `BaseModel` provides shared fields like `id`, `created_at`, and `updated_at`.
* `User`, `Place`, `Review`, and `Amenity` extend `BaseModel`.
* Cardinal relationships enforce data constraints and clarify ownership.

---

## 🔄 Sequence Diagrams for API Calls

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

This technical documentation consolidates the architectural structure, object models, and user interactions for the HBnB Evolution platform. It adheres to UML standards and is designed to be a reference for developers, testers, and stakeholders across all development stages. The use of layered architecture and sequence flows ensures clarity, scalability, and maintainability of the system.

---

**Author:** 
- Abdulelah Alsheri
- Muhannad Gsgs
- Abdulaziz Alzahrani
