<div align="center">

# ⚡ Scalable URL Shortener

### A production-oriented URL shortening service built with **Python + FastAPI**

<p>
<img src="https://img.shields.io/badge/Python-3.12%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
<img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
<img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=for-the-badge&logo=postgresql&logoColor=white" alt="PostgreSQL" />
<img src="https://img.shields.io/badge/Redis-DC382D?style=for-the-badge&logo=redis&logoColor=white" alt="Redis" />
</p>

<p>
<img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white" alt="SQLAlchemy" />
<img src="https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white" alt="Docker" />
<img src="https://img.shields.io/badge/Pytest-0A9EDC?style=for-the-badge&logo=pytest&logoColor=white" alt="Pytest" />
<img src="https://img.shields.io/badge/Ruff-261230?style=for-the-badge" alt="Ruff" />
</p>

</div>

---

## 🎯 Overview

**Scalable URL Shortener** is a backend-focused service for converting long URLs into compact, shareable links.

The project is built around **FastAPI, PostgreSQL, SQLAlchemy, Redis, Docker, and automated testing**, with scalability and production-readiness as long-term goals.

Rather than being just a basic CRUD application, the project explores real backend engineering concerns such as:

- Short-code generation
- Collision prevention
- Custom aliases
- URL expiration
- Fast redirect resolution
- Redis caching
- Persistent storage
- API error handling
- Containerized infrastructure
- Testing and code quality

---

## 🏗️ Architecture

```text
                         ┌─────────────────────┐
                         │      API Client     │
                         └──────────┬──────────┘
                                    │ HTTP
                                    ▼
                         ┌─────────────────────┐
                         │       FastAPI       │
                         │  Routing + Schemas  │
                         └──────────┬──────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
             ┌───────────────┐             ┌───────────────┐
             │  URL Service  │             │    /health    │
             │ Create/Lookup │             │ Health Check  │
             └───────┬───────┘             └───────────────┘
                     │
              ┌──────┴──────┐
              │             │
              ▼             ▼
       ┌──────────────┐ ┌──────────────┐
       │  PostgreSQL  │ │    Redis     │
       │  Persistence │ │ Read-through │
       │              │ │    Cache     │
       └──────────────┘ └──────────────┘
---
## Redirect Flow
GET /{short_code}
       │
       ▼
    Redis
       │
   ┌───┴────┐
   │        │
  hit      miss
   │        │
   │        ▼
   │   PostgreSQL
   │        │
   │   ┌────┴─────────────┐
   │   │                  │
   │  found            not found
   │   │                  │
   │   ▼                  ▼
   │ Validate          HTTP 404
   │ expiration
   │   │
   │   ├── expired ───► HTTP 410
   │   │
   │   ▼
   │ Cache result
   │
   └──────────► HTTP 307 Redirect
---
## 🚀 Current Functionality
Feature	Status
Short URL creation	✅
Cryptographically secure short codes	✅
Seven-character short codes	✅
Custom aliases	✅
Duplicate alias protection	✅
URL expiration	✅
Redis caching	✅
Expiration-aware Redis TTL	✅
Redirect endpoint	✅
404 handling	✅
410 expired URL handling	✅
PostgreSQL persistence	✅
SQLAlchemy ORM	✅
Health endpoint	✅
Alembic integration	🟡
Authentication	🟡
API rate limiting	🟡
Click analytics	🟡
QR code generation	🟡
Production deployment	🟡
Full CI/CD pipeline	🟡

✅ Implemented · 🟡 Planned

🔌 API
Create a Short URL
POST /urls
Content-Type: application/json
Request
{
  "original_url": "https://example.com/a/very/long/url",
  "custom_alias": "docs",
  "expires_at": "2026-12-31T23:59:59Z"
}

If custom_alias is omitted, the service automatically generates a unique seven-character short code.

Example Response
{
  "id": 1,
  "original_url": "https://example.com/a/very/long/url",
  "short_code": "docs",
  "short_url": "http://localhost:8000/docs",
  "custom_alias": "docs",
  "expires_at": "2026-12-31T23:59:59Z"
}
Redirect to Original URL
GET /{short_code}

Example:

GET /docs

A valid short code returns:

307 Temporary Redirect
Possible Responses
Status	Meaning
307	Redirect to original URL
404	Short URL does not exist
410	Short URL has expired
Health Check
GET /health

Example response:

{
  "status": "ok",
  "environment": "development"
}
🧠 Redis Caching Strategy

Redis is used on the short-code lookup path to reduce repeated database queries.

The lookup flow is:

Request
   │
   ▼
Redis lookup
   │
   ├── Cache HIT ─────► Return URL
   │
   └── Cache MISS
          │
          ▼
      PostgreSQL
          │
          ▼
   Validate expiration
          │
          ▼
      Cache URL
          │
          ▼
      Return URL

For URLs with an expiration time, the Redis cache entry receives a TTL based on the remaining lifetime of the URL.

This keeps cached data aligned with URL expiration semantics.

🔐 Short-Code Generation

When a custom alias is not provided, the service generates a random seven-character identifier.

The character set contains:

abcdefghijklmnopqrstuvwxyz
ABCDEFGHIJKLMNOPQRSTUVWXYZ
0123456789

The implementation uses Python's secrets module for random selection.

Generated codes are checked against existing database records before being persisted.

🛠️ Tech Stack
Layer	Technology
Language	Python 3.12+
API Framework	FastAPI
ASGI Server	Uvicorn
Validation	Pydantic
Configuration	Pydantic Settings
ORM	SQLAlchemy
Database	PostgreSQL 16
Cache	Redis 7
Migrations	Alembic
Testing	Pytest
HTTP Testing	HTTPX
Linting	Ruff
Infrastructure	Docker Compose
CI/CD	GitHub Actions
📁 Project Structure
scalable-url-shortener/
│
├── app/
│   │
│   ├── api/
│   │   └── routes/
│   │       ├── redirect.py
│   │       └── urls.py
│   │
│   ├── cache/
│   │   └── redis.py
│   │
│   ├── core/
│   │
│   ├── db/
│   │
│   ├── schemas/
│   │
│   ├── services/
│   │   └── url_service.py
│   │
│   └── main.py
│
├── tests/
│
├── alembic/
│
├── docker-compose.yml
├── pyproject.toml
└── README.md
🐳 Local Development
Prerequisites

Make sure you have:

Python 3.12+
Docker
Docker Compose
Git
1. Clone the Repository
git clone https://github.com/DixitDhruv-dev/scalable-url-shortener.git
cd scalable-url-shortener
2. Create a Virtual Environment
Windows PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
3. Install Dependencies
pip install -e ".[dev]"
4. Start PostgreSQL and Redis
docker compose up -d

This starts:

PostgreSQL → localhost:5432
Redis      → localhost:6379
5. Start the API
uvicorn app.main:app --reload

The API will be available at:

http://localhost:8000
📚 API Documentation

FastAPI automatically provides interactive API documentation.

Swagger UI
http://localhost:8000/docs
ReDoc
http://localhost:8000/redoc

These interfaces can be used to explore and test the API directly from your browser.

🧪 Testing

Run the test suite:

pytest

Run linting:

ruff check .

Development dependencies include:

pytest
httpx
ruff
🗄️ Infrastructure

The local development environment uses Docker Compose.

┌─────────────────────────────────────────┐
│             Docker Compose              │
│                                         │
│  ┌────────────────┐  ┌────────────────┐ │
│  │  PostgreSQL 16 │  │    Redis 7     │ │
│  │                │  │                │ │
│  │ Persistent DB  │  │ URL Cache      │ │
│  └────────────────┘  └────────────────┘ │
│                                         │
└─────────────────────────────────────────┘

PostgreSQL provides persistent URL storage.

Redis provides low-latency access to frequently requested short URLs.

📈 Scalability Roadmap

The project is designed to evolve from a single API instance into a horizontally scalable backend.

                    ┌───────────────┐
                    │ Load Balancer │
                    └───────┬───────┘
                            │
              ┌─────────────┼─────────────┐
              │             │             │
              ▼             ▼             ▼
         ┌─────────┐   ┌─────────┐   ┌─────────┐
         │ API #1  │   │ API #2  │   │ API #N  │
         └────┬────┘   └────┬────┘   └────┬────┘
              │             │             │
              └─────────────┼─────────────┘
                            │
                     ┌──────▼──────┐
                     │    Redis    │
                     └──────┬──────┘
                            │
                     ┌──────▼──────┐
                     │ PostgreSQL  │
                     └─────────────┘

Future engineering work includes:

Authentication and user accounts
API rate limiting
Click analytics
QR code generation
Metrics and observability
Structured logging
Production deployment
Horizontal API scaling
CI/CD automation
Database optimization
Improved cache invalidation
🔐 Engineering Priorities
Low-Latency Redirects

Redis reduces repeated PostgreSQL lookups for frequently accessed short URLs.

Collision Safety

Generated short codes are checked against existing records before insertion.

Consistent Expiration

Expiration is validated during lookup and reflected in Redis TTLs.

Separation of Responsibilities

The application separates:

API Layer
    ↓
Service Layer
    ↓
Database / Cache Layer

This keeps business logic independent from HTTP routing and infrastructure details.

Reproducible Development

Docker Compose provides consistent local PostgreSQL and Redis infrastructure.

🗺️ Roadmap
[x] FastAPI application foundation
[x] URL creation
[x] Random short-code generation
[x] Custom aliases
[x] Duplicate alias protection
[x] URL expiration
[x] Redis caching
[x] Redirect resolution
[x] PostgreSQL persistence
[x] Health endpoint
[x] Docker Compose infrastructure

[ ] Authentication & user accounts
[ ] API rate limiting
[ ] Click analytics
[ ] QR code generation
[ ] Metrics & observability
[ ] Production deployment
[ ] Horizontal scaling
[ ] Complete CI/CD pipeline
🤝 Contributing

Contributions, bug reports, and architectural discussions are welcome.

Typical workflow:

Fork
  ↓
Create branch
  ↓
Implement
  ↓
Test
  ↓
Lint
  ↓
Pull Request

For larger architectural changes, open an issue first to discuss the proposed approach.

👨‍💻 Author
<div align="center">
Dhruv Dixit

Backend Engineering · AI · Cloud · System Design

</div>
<div align="center">
⚡ Building systems that scale beyond the demo.

⭐ If you find this project interesting, consider giving it a star.

</div> ```
