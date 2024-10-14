# LATESHOW Code Challenge

## Table of Contents

- [LATESHOW Code Challenge](#lateshow-code-challenge)
  - [Table of Contents](#table-of-contents)
  - [Project Description](#project-description)
  - [Features](#features)
  - [Technologies Used](#technologies-used)
  - [Installation](#installation)
  - [Database Setup](#database-setup)
  - [API Endpoints](#api-endpoints)
    - [Welcome message](#welcome-message)
    - [Episodes](#episodes)
    - [Guests](#guests)
    - [Appearance](#appearance)
  - [Running the Application](#running-the-application)
  - [Testing](#testing)

---

## Project Description

This project is a RESTful API built with Flask. It is designed to manage `Episodes`, `Guests` and their `Appearances` on a late show. It demonstrates model relationships using SQLAlchemy, data validation, database migrations and API route handling.

---

## Features

- Retrieve and display episodes and guests.
- Create and display appearances of guests in episodes.
- Delete specific episodes.

---

## Technologies Used

- **Python**
- **Flask**: A lightweight web framework.
- **Flask-RESTful**: Extension to build REST APIs easily.
- **Flask-SQLAlchemy**: ORM (Object-relational mapper) for managing database interactions.
- **Flask-Migrate**: Handles database migrations.
- **SQLite**: Used as the database for this project.
- **Pipenv**: For dependency management and virtual environment.
- **SQLAlchemy-Serializer**: Enables easy serialization of SQLAlchemy models to JSON.

---

## Installation

To get started with the project, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/KoryrKoryr/Lateshow-Code-Challenge
   cd Lateshow-Code-Challenge
   ```
2. **Install Pipenv**:
   If you don't have Pipenv installed, install it via pip:

   ```bash
   pip install pipenv

   ```

3. **Install dependencies**:
   Use Pipenv to install project dependencies:

   ```bash
   pipenv install
   ```

4. **Activate the virtual environment**:
   After installing dependencies, activate the virtual environment:

   ```bash
   pipenv shell
   ```

---

## Database Setup

1. **Initialize the database**:
   Set up the database using Flask-Migrate:

   ```bash
   flask db init
   flask db migrate
   flask db upgrade head
   ```

2. **Seed the database**:
   The provided `seed.csv` file contains data on `episodes`, `guests`, and their `appearances`. Run the provided seed script:

   ```bash
   python seed.py
   ```

   This will read `seed.csv` file and populate the database with initial data.

---

## API Endpoints

Here are the available API endpoints:

### Welcome message

**GET /**: Returns a welcome message.

Response:

```

{
    "message": "Welcome to Lateshow Code Challenge API!"
}

```

### Episodes

**GET /episodes**: Fetches all episodes.
Example response:

```

[
    {
        "date": "1/11/99",
        "id": 1,
        "number": 1
    },
    {
        "date": "1/12/99",
        "id": 2,
        "number": 2
    }
]

```

**GET /episodes/**: Fetches a specific episode and its appearances.
Example response:

```
{
    "appearances": [
        {
            "episode_id": 1,
            "guest": {
                "id": 1,
                "name": "Michael J. Fox",
                "occupation": "actor"
            },
            "guest_id": 1,
            "id": 1,
            "rating": 5
        }
    ],
    "date": "1/11/99",
    "id": 1,
    "number": 1
}
```

**DELETE /episodes/**: Deletes a specific episode by its ID.
Example response (if the episode exists):

```
{
    "message": "Episode 1 deleted successfully"
}
```

Example response (if the episode does not exist):

```
{
    "error": "Episode not found"
}
```

### Guests

**GET /guests**: Fetches all guests.
Example response:

```
[
    {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
    },
    {
        "id": 2,
        "name": "Sandra Bernhard",
        "occupation": "Comedian"
    }
]
```

### Appearance

**POST /appearances**: Creates a new appearance for a guest on an episode.
Example request:

```
{
  "rating": 4,
  "episode_id": 2,
  "guest_id": 1
}
```

Example response (If the appearance is created successfully):

```
{
    "id": 162,
    "rating": 4,
    "guest_id": 1,
    "episode_id": 2,
    "episode": {
        "id": 2,
        "date": "1/12/99",
        "number": 2
    },
    "guest": {
        "id": 1,
        "name": "Michael J. Fox",
        "occupation": "actor"
    }
}
```

Response (If the appearance creation fails due to validation):

```
{
    "errors": [
        "Rating must be between 1 and 5"
    ]
}
```

Response (If the appearance creation fails due to missing resources):

```
{
    "errors": [
        "Episode or Guest not found"
    ]
}
```

## Running the Application

To run the application locally:

1.  **Activate the virtual environment**:

    ```bash
    pipenv shell
    ```

2.  **Run the Flask development server**:

    ```bash
    flask run
    ```

3.  **Access the API**:
    The Flask application will be available at http://127.0.0.1:5000 or http://localhost:5000.

---

## Testing

To test the API, you can use Postman or curl to make requests to the following endpoints:

- **GET /**
- **GET /episodes**
- **GET /guests/**
- **GET /episodes/**
- **DEL /episodes/**
- **POST /appearances**

Additionally, you can import the provided Postman collection (challenge-4-lateshow.postman_collection.json) to test all routes.

---
