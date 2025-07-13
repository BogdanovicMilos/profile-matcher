## Profile Matcher BE

Profile Matcher backend repository

## 🚀 Architecture Overview

The Profile Matcher API project implements a clean, modular, and layered backend architecture in `FastAPI` with `Python 3.12`. The application provides functionality to match player profiles to campaigns based on specific criteria, integrating with databases and external campaign APIs.


### Layers & Key Components:

- _API Layer_ - `application/`

   - Implements RESTful endpoints for interacting with the application.
   - Uses FastAPI routing and Pydantic models for request/response validation.
   - Handles dependency injection for database connections and other services.


- _Domain Layer_ - `domain/`

  - Contains the core business logic, including profile matching mechanisms.
  - Encapsulates rules for campaign-player matching using prioritized criteria.


- _Infrastructure Layer_ - `infrastructure/`
  - Manages database interactions using SQLAlchemy models.
  - Repository pattern abstracts data access logic.
  - Alembic migrations ensure seamless schema evolution.
  - Manages external API integrations for campaign data retrieval.


- _Testing_ - `tests/`
  - Pytest-based test suite with coverage reporting.
  - Organized by component for maintainability.


### Matching overview

1. The `/api/get_client_config/{player_id}` endpoint fetches the player profile based on the provided `UUID`.
2. Campaigns are retrieved using the `CampaignService`.
3. The `CampaignMatcher` compares player attributes (level, country, items) with campaign rules to generate matching campaigns.
4. If the matched campaigns differ from the player's current active campaigns, the database is updated.


### User Initialization
- At startup, a `Player` is created and added to the database using the initialization logic in `player_initializer.py`. This helps ensure there’s base data available for testing and development purposes.


<hr></hr>


## 📦 Setup

### Step 1: Create virtual environment:
```bash
python3 -m venv .venv
```

Activate virtual environment:
```bash
source .venv/bin/activate
```

### Step 2: Create environment variables files

- Copy `example.env` to `.env` and set the variables.

- Copy `example.env.docker` to `.env.docker` and set the variables.

### Step 3: Configure `settings.py` file:

For local development:
> model_config = SettingsConfigDict(
    env_file=".env",
    env_file_encoding="utf-8",
)

For docker compose (default):
> model_config = SettingsConfigDict(
    env_file=".env.docker",
    env_file_encoding="utf-8",
)


### Step 4: Configure `pre-commit` (Optional)
Install pre-commits:
```bash
pre-commit install
```
Run pre-commits:
```bash
pre-commit run --all-files
```

## ▶️ Run development server
Install dependencies:
```bash
pip3 install -r requirements.txt -r requirements.dev.txt
```

Run migrations:
```bash
alembic upgrade head
```

Run server:
```bash
uvicorn application.api.main:app --host 0.0.0.0 --port 8000 --reload
```


## ▶️ Run using docker compose

Run docker compose:
```bash
docker compose up --build
```

Remove all containers, networks, images, and volumes:
```bash
docker compose down -v
```

## 🧪 Tests and coverage

Get the test coverage by running:
```bash
coverage run -m pytest tests/*
```
To get the report:
```bash
coverage report -m
```
or to get HTML version:
```bash
coverage html
```

## 🛠️ API Endpoints

The API documentation is automatically generated and accessible locally:

- [Documentation](http://localhost:8000/docs)
