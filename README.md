# Garage AI

Garage AI is a modern garage management system built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **OpenAI GPT-5**.

The application helps automotive workshops manage customers, vehicles, and repair jobs while leveraging AI to generate professional repair diagnostics that assist technicians during vehicle inspections and servicing.

---

# Features

## Authentication

- JWT Authentication
- Secure user login
- Protected API endpoints

## Customer Management

- Create customers
- View customer records
- Delete customers

## Vehicle Management

- Register vehicles
- Link vehicles to customers
- View all registered vehicles
- Delete vehicles

## Repair Job Management

- Create repair jobs
- Record customer complaints
- Track mileage
- Manage repair status
- Store technician notes
- Delete repair jobs

## AI Repair Diagnosis

Generate AI-powered repair recommendations using **OpenAI GPT-5**.

The AI analyzes:

- Vehicle information
- Repair title
- Customer complaint
- Mileage

It then generates:

- Possible causes
- Recommended inspections
- Recommended repairs
- Estimated urgency

Diagnoses are automatically saved to the database and can be viewed later without regenerating them.

---

# Technology Stack

## Backend

- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic
- Pydantic
- JWT Authentication

## Frontend

- HTML5
- Bootstrap 5
- Vanilla JavaScript

## Artificial Intelligence

- OpenAI Python SDK
- GPT-5
- Responses API

---

# Project Structure

```text
garage-ai/
│
├── alembic/
│
├── app/
│   ├── api/
│   │   └── v1/
│   │
│   ├── core/
│   ├── models/
│   ├── repositories/
│   ├── schemas/
│   ├── services/
│   ├── static/
│   │   └── js/
│   ├── templates/
│   ├── database.py
│   └── main.py
│
├── .env
├── requirements.txt
└── README.md
```

---

# Getting Started

## 1. Clone the Repository

```bash
git clone https://github.com/lazarustanaka11/garage-ai.git

cd garage-ai
```

---

## 2. Create a Virtual Environment

### Windows

```bash
python -m venv .venv

.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv

source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# PostgreSQL Setup

Create a PostgreSQL database.

Example database:

```
garage_ai
```

Update your PostgreSQL credentials in the `.env` file.

---

# Environment Variables

Create a file named:

```
.env
```

Example:

```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/garage_ai

SECRET_KEY=your_secret_key_here

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

OPENAI_API_KEY=your_openai_api_key
```

Replace:

- `password`
- `your_secret_key_here`
- `your_openai_api_key`

with your own values.

---

# Database Migration

Run the Alembic migrations:

```bash
alembic upgrade head
```

---

# Running the Application

Start the development server:

```bash
uvicorn app.main:app --reload
```

Application:

```
http://127.0.0.1:8000
```

Swagger API Documentation:

```
http://127.0.0.1:8000/docs
```

---

# Using the Application

## Customers

Create and manage customer records.

## Vehicles

Register vehicles and assign them to customers.

## Repair Jobs

Create repair jobs with:

- Vehicle
- Title
- Description
- Mileage

Track repair progress throughout the repair process.

---

# AI Diagnosis

Open the **Repair Jobs** page.

For any repair job without an existing diagnosis, click:

```
Diagnose
```

Garage AI sends the repair details to **OpenAI GPT-5**, which generates:

- Possible causes
- Recommended inspections
- Recommended repairs
- Estimated urgency

The diagnosis is automatically saved to the database.

Previously generated diagnoses can be viewed at any time using the **View AI** button.

---

# REST API

Interactive API documentation is available through Swagger:

```
http://127.0.0.1:8000/docs
```

---

# Current Functionality

- JWT Authentication
- Customer Management
- Vehicle Management
- Repair Job Management
- AI Repair Diagnosis
- PostgreSQL Database
- Bootstrap Frontend
- REST API Architecture

---

# Architecture

The application follows a layered architecture.

```
Router
    │
    ▼
Service
    │
    ▼
Repository
    │
    ▼
Database
```

The AI module follows the same pattern.

```
AI Router
      │
      ▼
RepairJobService
      │
      ▼
OpenAIService
      │
      ▼
OpenAI Responses API
```

This keeps business logic separated from API routes and makes the application easier to maintain, extend, and test.

---

# Future Improvements

Planned features include:

- AI Repair Cost Estimates
- AI Parts Recommendations
- AI Customer-Friendly Repair Summaries
- AI Maintenance Recommendations
- Technician Dashboard
- Customer Portal
- Vehicle Service History
- File Uploads
- Vehicle Images
- PDF Repair Reports
- Email Notifications
- Analytics Dashboard

---

# Screenshots

Screenshots will be added as the project evolves.

---

# License

This project is intended for educational, learning, and portfolio purposes.

---

# Author

**Lazarus Tanaka Mtake**

Software Developer

GitHub: https://github.com/lazarustanaka11
