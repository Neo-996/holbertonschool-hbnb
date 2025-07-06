# HBnB Project - Part 2: Business Logic & API Implementation

## 📚 Overview

This part of the **HBnB project** focuses on implementing the **Business Logic** and **Presentation Layers** using **Python**, **Flask**, and **flask-restx**. The goal is to create a modular, scalable foundation for the application that includes core functionality for managing **Users**, **Places**, **Reviews**, and **Amenities** via a RESTful API.

---

## 🏗️ Project Structure

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── users.py
│   │   │   ├── places.py
│   │   │   ├── reviews.py
│   │   │   ├── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   ├── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── facade.py
│   ├── persistence/
│   │   ├── __init__.py
│   │   ├── repository.py
├── run.py
├── config.py
├── requirements.txt
├── README.md
```

---

## 🎯 Objectives

- Organize the project using best practices for Flask applications.
- Implement business logic for core models: `User`, `Place`, `Review`, and `Amenity`.
- Use the **facade design pattern** for interaction between layers.
- Build RESTful API endpoints with **flask-restx** for CRUD operations.
- Serialize nested data (e.g., a `Place` includes owner details and amenity names).
- Ensure the API is testable and handles edge cases gracefully.

---

## 🚀 Getting Started

### 🔧 Installation

```bash
# Clone the repo
git clone https://github.com/Neo-996/holbertonschool-hbnb.git
cd holbertonschool-hbnb

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

---

### ▶️ Running the App

```bash
python run.py
```

The API will be available at:  
**http://localhost:5000/**  
The Swagger UI (interactive docs) will be available at:  
**http://localhost:5000/docs**

---

## 📡 API Endpoints

**Base Path:** `/api/v1`

### Users
- `GET /users/`
- `GET /users/<id>`
- `POST /users/`
- `PUT /users/<id>`
- `DELETE /users/<id>`

### Places
- `GET /places/`
- `GET /places/<id>`
- `POST /places/`
- `PUT /places/<id>`
- `DELETE /places/<id>`

### Reviews
- `GET /reviews/`
- `GET /reviews/<id>`
- `POST /reviews/`
- `PUT /reviews/<id>`
- `DELETE /reviews/<id>`

### Amenities
- `GET /amenities/`
- `GET /amenities/<id>`
- `POST /amenities/`
- `PUT /amenities/<id>`
- `DELETE /amenities/<id>`

Each endpoint returns structured JSON, including related data where applicable.

---

## 🧠 Key Concepts

- **Modular Architecture**: Clear separation between layers for maintainability.
- **Facade Pattern**: Simplifies API logic by abstracting interactions with business services.
- **Data Serialization**: Responses include related fields (e.g., user names, amenity names).
- **Versioning**: API is namespaced under `/api/v1` for future expansion.

---

## 🛠️ Technologies Used

- **Python 3.11+**
- **Flask**
- **flask-restx**
- **Flask-RESTful Concepts**
- **Virtualenv**

---

## ✅ Testing

Use tools like **Postman** or `curl` to test endpoints.

Example:

```bash
curl -X GET http://localhost:5000/api/v1/users/
```

---

## 🚫 Not Included in This Part

- 🔒 JWT Authentication  
- 🔐 Role-Based Access Control  

---

## 📘 References

- [Flask Docs](https://flask.palletsprojects.com/)
- [flask-restx Docs](https://flask-restx.readthedocs.io/)
- [RESTful API Best Practices](https://docs.microsoft.com/en-us/azure/architecture/best-practices/api-design)
- [Facade Design Pattern in Python](https://refactoring.guru/design-patterns/facade/python/example)

---

## 👥 Authors

- **Abdulaziz Alzahrani**  
- **Abdulelah Alshehri**  
- **Muhannad Gsgs**  

---

## 📄 License

This project is licensed under the **MIT License**.
