# TRACE ONWARD AI

TRACE ONWARD AI is a Flask-based AI assistant and lead management system integrated with a Wix Studio website.

The project adapts the SmartLead AI assignment architecture to TRACE ONWARD, a social travel platform built around real journeys, discovery, and remixing travel experiences.

## Live Links

- Wix Website: https://mirayderici0.wixstudio.com/my-site-5
- Render Backend: https://trace-onward-ai.onrender.com
- GitHub Repository: https://github.com/mirayderici0/trace-onward-ai

## Main Features

- Ask TRACE AI assistant on the Wix website
- AI responses generated through the Groq API
- Early Access lead form with name, phone, and message
- SQLite lead storage
- Wix Dashboard with a Repeater that displays saved leads
- Contact page with a working Wix form
- Flask REST API deployed on Render
- Separation of concerns between configuration, database, routes, and AI service

## System Flow

```text
User
  ↓
Wix Studio Website
  ├── Ask TRACE
  │      ↓
  │   Flask API
  │      ↓
  │   Groq AI
  │
  └── Early Access Form
         ↓
      Flask API
         ↓
      SQLite
         ↓
      Wix Lead Dashboard
```

## Project Structure

```text
trace_onward_ai/
│
├── run.py
├── config.py
├── requirements.txt
├── .env
├── .gitignore
│
└── app/
    ├── __init__.py
    ├── database.py
    ├── routes.py
    │
    ├── templates/
    │   ├── index.html
    │   └── dashboard.html
    │
    └── services/
        ├── __init__.py
        └── ai_service.py
```

## Architecture

The project follows separation of concerns:

- `config.py` manages environment-based configuration and TRACE ONWARD business context.
- `database.py` contains SQLite connection and lead database operations.
- `ai_service.py` contains the Groq AI integration and AI-related error handling.
- `routes.py` defines the Flask web and API routes.
- `app/__init__.py` creates and configures the Flask application.
- `run.py` starts the application.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | Main backend page |
| GET | `/dashboard` | Flask lead dashboard |
| GET | `/health` | Health check |
| POST | `/api/sohbet` | Sends a user message to TRACE AI |
| POST | `/api/leads` | Saves a new lead |
| GET | `/api/leads` | Returns saved leads |

## Local Installation

### 1. Clone the repository

```bash
git clone https://github.com/mirayderici0/trace-onward-ai.git
cd trace-onward-ai
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a `.env` file

Example:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=trace_onward.db
GROQ_API_KEY=your-groq-api-key
AI_PROVIDER=groq
```

Do not commit the `.env` file to GitHub.

### 5. Run the application

```bash
python run.py
```

The local server runs on:

```text
http://127.0.0.1:5000
```

## Testing

Health check:

```text
GET /health
```

AI request example:

```json
POST /api/sohbet

{
  "message": "What is TRACE ONWARD?",
  "history": []
}
```

Lead request example:

```json
POST /api/leads

{
  "name": "Test User",
  "phone": "05551112233",
  "message": "Interested in early access"
}
```

Saved leads can be checked with:

```text
GET /api/leads
```

## Wix Integration

The Wix Studio frontend communicates with the Flask backend through Velo backend web methods.

The website includes:

- Ask TRACE message input
- Ask button
- AI response area
- Early Access name, phone, and message fields
- Lead save button
- Lead Dashboard using a Wix Repeater
- Contact page
- Navigation links to Home, How It Works, Dashboard, Contact, and Join Early Access

## Security

- API keys and secrets are stored in environment variables.
- `.env` is excluded through `.gitignore`.
- SQLite queries use parameterized placeholders.
- AI and database logic are separated from route logic.
- API errors are handled with controlled responses.

## Deployment

The Flask backend is deployed on Render.

Build command:

```bash
pip install -r requirements.txt
```

Start command:

```bash
gunicorn run:app
```

Required secret values are stored in Render Environment Variables.

## Demo Note

SQLite is used for this MVP and assignment demonstration. For a production system, persistent managed database storage would be preferable.

## Project Goal

TRACE ONWARD AI demonstrates how an AI assistant, lead collection flow, backend API, database, deployment service, and Wix Studio frontend can work together in one modular project.

The user can ask TRACE about the platform, leave early-access information, and the saved lead can then be viewed from the Wix Dashboard.
