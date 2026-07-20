# 🚗 Garage AI

Garage AI is a modern AI-powered garage management platform built with
**FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **OpenAI GPT-5**.

The application enables automotive workshops to manage customers,
vehicles, and repair jobs while generating intelligent repair
recommendations using the OpenAI Responses API.

------------------------------------------------------------------------

# 🚀 Live Demo

Application: https://garage-ai-xx03.onrender.com/

Swagger API: https://garage-ai-xx03.onrender.com/docs

------------------------------------------------------------------------

# ✨ Project Highlights

-   🚀 Live deployment on Render
-   🤖 AI-powered repair diagnostics with OpenAI GPT-5
-   🐳 Docker & Docker Compose support
-   🔐 JWT Authentication
-   🗄 PostgreSQL with Alembic migrations
-   🏗 Repository → Service → Router architecture
-   📖 Interactive Swagger documentation
-   ☁️ Cloud-ready deployment

------------------------------------------------------------------------

# Features

## Authentication

-   JWT Authentication
-   Secure Login
-   Protected Endpoints

## Customer Management

-   Create, view and delete customers

## Vehicle Management

-   Register vehicles
-   Assign vehicles to customers
-   View and delete vehicles

## Repair Jobs

-   Create repair jobs
-   Track mileage
-   Store technician notes
-   Update repair status

## AI Diagnostics

Generates: - Possible causes - Recommended inspections - Recommended
repairs - Repair urgency

------------------------------------------------------------------------

# Technology Stack

## Backend

-   Python
-   FastAPI
-   SQLAlchemy 2.0
-   PostgreSQL
-   Alembic
-   Pydantic
-   JWT Authentication

## Frontend

-   HTML5
-   Bootstrap 5
-   Vanilla JavaScript

## AI

-   OpenAI Python SDK
-   GPT-5 Responses API

## DevOps

-   Docker
-   Docker Compose
-   Render

------------------------------------------------------------------------

# Project Structure

``` text
garage-ai/
├── alembic/
├── app/
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
├── requirements.txt
├── .env
└── README.md
```

------------------------------------------------------------------------

# Local Installation

``` bash
git clone https://github.com/lazarustanaka11/garage-ai.git
cd garage-ai
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env`

``` env
DATABASE_URL=postgresql://postgres:password@localhost:5432/garage_ai
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OPENAI_API_KEY=your_openai_api_key
```

Run:

``` bash
alembic upgrade head
uvicorn app.main:app --reload
```

------------------------------------------------------------------------

# Docker

``` bash
docker compose up --build
```

Docker automatically:

-   Starts PostgreSQL
-   Waits for health checks
-   Runs Alembic migrations
-   Starts FastAPI

Application: - http://localhost:8000 - http://localhost:8000/docs

Stop:

``` bash
docker compose down
```

------------------------------------------------------------------------

# Deployment

Production: https://garage-ai-xx03.onrender.com/

Swagger: https://garage-ai-xx03.onrender.com/docs

------------------------------------------------------------------------

# Architecture

``` text
Router
  ↓
Service
  ↓
Repository
  ↓
Database
```

AI Flow

``` text
AI Router
  ↓
RepairJobService
  ↓
OpenAIService
  ↓
OpenAI Responses API
```

------------------------------------------------------------------------

# Current Functionality

-   JWT Authentication
-   Customer Management
-   Vehicle Management
-   Repair Jobs
-   AI Diagnostics
-   PostgreSQL
-   Docker
-   Docker Compose
-   Alembic Migrations
-   REST API
-   Render Deployment

------------------------------------------------------------------------

# Future Improvements

-   AI Cost Estimates
-   Parts Recommendations
-   Maintenance Scheduling
-   Customer Portal
-   File Uploads
-   PDF Reports
-   Email Notifications
-   Analytics Dashboard

------------------------------------------------------------------------

# License

Portfolio project.

------------------------------------------------------------------------

# Author

**Lazarus Tanaka Mtake**

GitHub: https://github.com/lazarustanaka11

LinkedIn: https://www.linkedin.com/in/lazarus-tanaka-mtake-9b5b081a2/
