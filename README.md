# AI Prompt Library

A full-stack application for managing AI Image Generation Prompts.

## Tech Stack

- **Frontend**: Angular 19 (standalone components)
- **Backend**: Django 4 (plain views, no DRF)
- **Database**: PostgreSQL 15
- **Cache**: Redis (view counter)
- **Container**: Docker + Docker Compose

## Quick Start

```bash
docker-compose up --build
```

- Frontend: http://localhost:4200
- Backend API: http://localhost:8000/prompts/

## API Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| GET | `/prompts/` | List all prompts |
| POST | `/prompts/` | Create a new prompt |
| GET | `/prompts/:id/` | Get prompt + increment view count |

### POST /prompts/ payload

```json
{
  "title": "Cyberpunk City",
  "content": "A neon-lit futuristic cityscape at night...",
  "complexity": 7
}
```

## Features

- Prompt list with title and complexity displayed as cards
- Prompt detail view with live view counter (Redis-backed)
- Add prompt form with reactive validation (title ≥ 3 chars, content ≥ 20 chars, complexity 1–10)
- Full Docker Compose setup (PostgreSQL + Redis + Django + Angular via nginx)

## Architectural Decisions

**No DRF** — Plain Django `JsonResponse` views keep the backend minimal and dependency-light, matching the assignment spec.

**Redis view counter** — `cache.incr()` is atomic and fast. Redis is the sole source of truth for view counts; they are not persisted to PostgreSQL. On first access the key is initialized to 1.

**nginx as frontend server** — The Angular app is built to static files and served by nginx. nginx also proxies `/prompts/` to the Django backend, so the frontend uses relative URLs and avoids CORS issues in production.

**Health checks** — The backend waits for both `db` and `redis` to be healthy before starting, preventing startup race conditions.

## Local Development (without Docker)

**Backend**
```bash
cd backend/app
pip install -r requirements.txt
# Requires a local PostgreSQL and Redis, or update settings.py to use SQLite
python manage.py migrate
python manage.py runserver
```

**Frontend**
```bash
cd frontend
npm install
# Update src/app/services/prompt.service.ts apiUrl to http://localhost:8000/prompts/
npm start
```
