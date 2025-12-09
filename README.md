
# QuizMaster Backend Documentation

QuizMaster is a Flask-based backend that provides authentication, CRUD operations, statistics, Redis-backed rate limiting, and asynchronous email delivery using Celery. This README describes the backend architecture, environment configuration, endpoints, and how to run all services.

---

# Overview

The backend exposes a REST API that handles:

- User and admin authentication (JWT)
- CRUD operations for subjects, chapters, quizzes, questions, and users
- User quiz interactions and performance statistics
- Subject-level statistics
- Rate limiting using Redis
- Celery tasks for asynchronous operations, including emailing subject statistics

SQLite is used as the default database, via SQLAlchemy and raw SQL for aggregations.



---

# Environment Variables (`backend/.env`)

The backend requires a `.env` file to configure Flask, Redis, Celery, and SMTP.


# Flask

SECRET_KEY=supersecretkey
FLASK_ENV=development
FLASK_DEBUG=1

# Database (SQLite default)

DATABASE_URL=sqlite:///instance/db.sqlite3

# Redis (Limiter + Celery Broker + Result Backend)

REDIS_URL=redis://localhost:6379/0
RATELIMIT_STORAGE_URL=redis://localhost:6379/2
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/1

# SMTP for Celery Email Task

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=[your_email@gmail.com](mailto:your_email@gmail.com)
SMTP_PASS=your_app_password
FROM_EMAIL=[your_email@gmail.com](mailto:your_email@gmail.com)

```

Notes:

- Gmail requires enabling 2FA and creating an App Password.
- Mailtrap SMTP credentials may be used for development testing.

---

# Redis Rate Limiting

Flask-Limiter uses Redis as its storage backend.

Configuration:

```

RATELIMIT_STORAGE_URL=redis://localhost:6379/2

````

Endpoints include decorators such as:

```python
@limiter.limit("100 per minute")
````

Redis stores rate-limit counters, enabling IP-based or user-based throttling.

---

# Celery Integration

Celery is configured in `celery_app.py` using Redis as both broker and result backend. A Celery worker must be running for asynchronous tasks.

The primary Celery task:

```
tasks/subject_stats.py
```

This task:

1. Executes raw SQL to compute subject statistics.
2. Generates a plain-text email body.
3. Sends the email using SMTP credentials defined in `.env`.
4. Supports retries and logs task failures.

Endpoints related to Celery:

```
POST /email-subject-stats       # Enqueues the Celery task
GET  /tasks/<task_id>           # Retrieves Celery task state and result
```

---

# API Endpoints

## Authentication

```
POST /login
POST /signup
POST /adminlogin
```

## Subjects

```
POST   /createsubject
GET    /getsubjects
PUT    /editsubject/<id>
DELETE /deletesubject/<id>
```

## Chapters

```
POST   /createchapter/<subject_id>
PUT    /editchapter/<chapter_id>
DELETE /deletechapter/<chapter_id>
GET    /getchapter/<subject_id>
```

## Quizzes

```
POST   /createquiz/<chapter_id>
GET    /getquiz/<chapter_id>
PUT    /editquiz/<quiz_id>
DELETE /deletequiz/<quiz_id>
```

## Questions

```
POST   /createquestion/<quiz_id>
GET    /getquestion/<quiz_id>
PUT    /editquestion/<question_id>
DELETE /deletequestion/<question_id>
```

## Statistics

```
GET /getcounts
GET /subjectstats
```

## Celery Email Endpoints

```
POST /email-subject-stats       # Body: { "email": "example@mail.com" }
GET  /tasks/<task_id>
```

---

# Running the Backend

## Install Dependencies

```
cd backend
pip install -r requirements.txt
```

## Start Redis

```
redis-server
```

## Run Flask Server

```
python main.py
```

## Run Celery Worker

```
cd backend
celery -A celery_app.celery worker --loglevel=info
```

(Optional) Celery Beat (if scheduled tasks are introduced):

```
celery -A celery_app.celery beat --loglevel=info
```

---

# Manual Email Test

```
import os, smtplib
from dotenv import load_dotenv

load_dotenv()

s = smtplib.SMTP(os.getenv("SMTP_HOST"), int(os.getenv("SMTP_PORT")))
s.starttls()
s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASS"))
s.sendmail(os.getenv("FROM_EMAIL"), "target@example.com", "Subject: Test\n\nHello")
s.quit()
```

---

# Database Notes

* SQLite database stored in `backend/instance/db.sqlite3`
* SQLAlchemy ORM used for standard CRUD operations
* Raw SQL used for aggregated statistics queries such as `/subjectstats`

Example aggregation query:

```
SELECT s.id, s.name,
       (SELECT COUNT(*) FROM usersubject WHERE subject_id = s.id) AS user_count,
       (SELECT AVG(sc.score)
        FROM quiz q
        JOIN chapter c ON q.chapter_id = c.id
        JOIN scores sc ON sc.quiz_id = q.id
        WHERE c.subject_id = s.id
       ) AS avg_score
FROM subject s;
```

---

# Summary

The QuizMaster backend includes:

* Flask REST API
* JWT authentication
* Redis-backed rate limiting
* Celery for asynchronous email tasks
* SQLite database with ORM and raw SQL
* Full endpoint suite for managing quizzes, users, subjects, and chapters
* Async statistics email via `/email-subject-stats`


