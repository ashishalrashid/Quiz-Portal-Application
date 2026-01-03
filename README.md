

# QuizMaster — Full Stack Application (Vue + Flask + Celery + Redis)

QuizMaster is a web-based application for managing subjects, chapters, quizzes, and questions. It includes authentication, role-based access control, CRUD operations, statistics, rate limiting, and asynchronous email sending using Celery.

---

# Tech Stack

## Frontend

* Vue 3
* Vite
* Vue Router
* Chart.js
* FontAwesome

## Backend

* Flask + Flask-RESTful
* SQLite with SQLAlchemy ORM and raw SQL
* Flask-JWT-Extended
* Flask-Limiter (Redis backed)
* Celery + Redis for asynchronous tasks
* SMTP or Mailtrap for transactional email

---

# Frontend Overview

## Directory Structure

```
frontend/
├── index.html
├── src/
│   ├── main.js
│   ├── App.vue
│   ├── router/
│   ├── views/
│   ├── components/
│   ├── assets/
│   └── style.css
└── public/
```

## Frontend Features

* User dashboard for taking quizzes and viewing performance
* Admin dashboard for managing users, subjects, chapters, quizzes, and questions
* Dynamic routing with Vue Router
* Chart.js visualizations
* Modular component-based UI

## Setup

```bash
npm install
npm run dev
npm run build
```

---

# Backend Overview

## Directory Structure

```
backend/
├── app.py
├── main.py
├── config.py
├── extensions.py
├── models.py
├── routes/
│   ├── auth.py
│   ├── admin.py
│   ├── user.py
│   ├── stats.py
│   └── email_stats.py
├── tasks/
│   └── subject_stats.py
├── celery_app.py
├── cache.py
├── testdb.py
└── requirements.txt
```

---

# Backend Features (Combined)

## Authentication and Access Control

* JWT-based user and admin authentication
* Role-based access management

## CRUD Operations

* Full CRUD for users, subjects, chapters, quizzes, and questions
* Implemented using both SQLAlchemy ORM and raw SQL when needed for performance or flexibility

## Statistics

* Count statistics (`/getcounts`)
* Subject statistics (`/subjectstats`)
* Uses optimized raw SQL aggregation

## Search

* Supports search across users, subjects, quizzes, and questions

## Rate Limiting

* Configured using Flask-Limiter
* Redis is used as the rate-limiting storage

## New Features (Celery and Redis Integration)

### Asynchronous Emailing of Subject Statistics

* A Celery worker handles sending subject statistics via SMTP
* Non-blocking operations ensure API responsiveness

### Task Status Monitoring

* Tasks return a task ID
* Users can check the status and result of tasks through a dedicated endpoint

### SMTP Email Integration

* Works with Gmail App Password, Mailtrap, or SendGrid
* Email content is generated from live subject statistics data

---

# API Endpoints (Combined)

## Authentication

* POST `/login`
* POST `/signup`
* POST `/adminlogin`

## Subjects

* POST `/createsubject`
* PUT `/editsubject/<id>`
* DELETE `/deletesubject/<id>`
* GET `/getsubjects`

## Chapters

* POST `/createchapter/<subject_id>`
* PUT `/editchapter/<id>`
* DELETE `/deletechapter/<id>`
* GET `/getchapter/<subject_id>`

## Quizzes

* POST `/createquiz/<chapter_id>`
* PUT `/editquiz/<id>`
* DELETE `/deletequiz/<id>`
* GET `/getquiz/<chapter_id>`

## Questions

* POST `/createquestion/<quiz_id>`
* PUT `/editquestion/<id>`
* DELETE `/deletequestion/<id>`
* GET `/getquestion/<quiz_id>`

## Statistics

* GET `/getcounts`
* GET `/subjectstats`

## New Async Email Endpoints

* POST `/email-subject-stats`
  Body: `{ "email": "recipient@example.com" }`
  Returns a Celery `task_id`.

* GET `/tasks/<task_id>`
  Returns Celery task status and result.

---

# Environment Variables (`backend/.env`)

```
FLASK_ENV=development
SECRET_KEY=supersecretkey

DATABASE_URL=sqlite:///instance/db.sqlite3

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1
RATELIMIT_STORAGE_URL=redis://localhost:6379/2

# SMTP
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASS=your_app_password
FROM_EMAIL=your_email@gmail.com
```

---

# Backend Setup

## Install dependencies

```bash
cd backend
pip install -r requirements.txt
```

## Start Redis

Local or remote Redis can be used.

## Initialize database (if required)

```bash
python testdb.py
```

## Run Flask API server

```bash
python main.py
```

## Start Celery worker

```bash
celery -A celery_app.celery worker --loglevel=info
```



---

# Celery Workflow Summary

1. A user sends a POST request to `/email-subject-stats`.
2. The API triggers a Celery task and immediately returns a task ID.
3. The Celery worker reads the job from Redis.
4. It computes subject statistics, composes the email, and sends it using SMTP.
5. Task status and result can be checked through `/tasks/<task_id>`.

---

