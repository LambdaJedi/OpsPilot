# OpsPilot

**A business process automation platform for managing internal purchase requests and approval workflows.**

OpsPilot is an ongoing portfolio project exploring how business processes can be digitised and automated using Python, REST APIs, relational databases and workflow orchestration.

The current implementation focuses on purchase request submission, rule-based approval routing and request management.

## Dashboard

![OpsPilot Dashboard](docs/screenshots/dashboard.png)

*Dashboard screenshot will be added as development progresses.*

## The problem

Businesses often manage internal purchase requests through emails, spreadsheets and disconnected approval processes. This can make requests difficult to track and approvals difficult to manage.

OpsPilot aims to provide a centralised workflow where employees can submit requests, approval requirements are determined by business rules, and relevant stakeholders can process them.

## Technology stack

| Technology | Purpose |
|---|---|
| Python | Backend application logic |
| FastAPI | REST API |
| PostgreSQL | Persistent data storage |
| SQLAlchemy | Database ORM |
| Alembic | Database migrations |
| HTML, CSS and JavaScript | Frontend dashboard |
| Docker Compose | Local service orchestration |
| n8n | Planned workflow orchestration |
| Ollama | Planned local AI integration |

## Current functionality

- Submit purchase requests through a web form.
- Validate incoming request data through the FastAPI backend.
- Persist purchase requests in PostgreSQL.
- Retrieve and display purchase requests through the API and dashboard.
- Determine approval routes based on purchase amounts.
- Create the required manager and finance approval records.
- Maintain database schema changes through Alembic migrations.

### Approval routing rules

| Purchase amount | Approval route |
|---|---|
| R0 – R1,999.99 | Automatic approval eligibility |
| R2,000 – R19,999.99 | Manager approval |
| R20,000 and above | Manager and finance approval |

Automatic approval eligibility is currently a routing classification. The full automatic policy-checking workflow is still under development.

## Architecture

The current application follows a layered architecture:

```text
Employee
   |
   v
Frontend Dashboard
   |
   v
FastAPI REST API
   |
   +---- Request validation
   |
   +---- Approval routing
   |
   +---- Approval workflow services
   |
   v
SQLAlchemy
   |
   v
PostgreSQL
```

Planned workflow orchestration and integrations will extend this architecture as development continues.

## Running locally

### Prerequisites

- Python 3.11+
- Docker Desktop
- Git

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd OpsPilot
```

### 2. Configure environment variables

Copy the example environment file:

**PowerShell:**

```powershell
Copy-Item .env.example .env
```

Update `.env` with your own secure passwords and encryption key. Do not commit this file.

### 3. Start the Docker services

```powershell
docker compose up -d
```

This starts PostgreSQL and n8n.

### 4. Set up the Python environment

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
```

### 5. Apply database migrations

```powershell
alembic upgrade head
```

### 6. Start the backend

```powershell
uvicorn backend.app.main:app --reload
```

The API will be available at:

- API: http://127.0.0.1:8000
- Interactive API documentation: http://127.0.0.1:8000/docs

### 7. Start the frontend

Open another terminal from the project root:

```powershell
python -m http.server 5500 --directory frontend
```

Open the dashboard at:

http://127.0.0.1:5500

## Testing

Run the test suite from the project root:

```powershell
python -m pytest
```

## Development roadmap

- [x] Purchase request submission and persistence
- [x] Rule-based approval routing
- [x] Manager and finance approval record creation
- [x] Database migrations
- [x] Initial approval decision service
- [ ] Approval decision API endpoints
- [ ] Approval history and audit logging
- [ ] Dashboard approval management
- [ ] n8n workflow orchestration
- [ ] Simulated ERP integration
- [ ] CSV and XML data exchange
- [ ] Local AI-assisted request classification
- [ ] Expanded automated testing

## Project status

OpsPilot is actively under development. Features listed in the development roadmap are not necessarily implemented yet.

The project is intended as a practical demonstration of backend development, database design, business process automation and system integration.

## Author

**Njabulo Ncube**

GitHub: [LambdaJedi](https://github.com/LambdaJedi)
