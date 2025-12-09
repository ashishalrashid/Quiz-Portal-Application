import os
import smtplib
from email.mime.text import MIMEText
from celery import Task
from celery.utils.log import get_task_logger
from celery_app import celery
from sqlalchemy import text
from models import db 

logger = get_task_logger(__name__)

SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER", "your_email@gmail.com")
SMTP_PASS = os.getenv("SMTP_PASS", "your_app_password")
FROM_EMAIL = os.getenv("FROM_EMAIL", SMTP_USER)


class DatabaseTask(Task):
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        try:
            db.session.remove()
        except Exception:
            pass
        return super().after_return(status, retval, task_id, args, kwargs, einfo)


def _fetch_subject_stats():
    sql = text("""
        SELECT s.id, s.name,
          (SELECT COUNT(*) FROM usersubject us WHERE us.subject_id = s.id) as user_count,
          (SELECT AVG(sc.score)
           FROM quiz q
           JOIN chapter c ON q.chapter_id = c.id
           JOIN scores sc ON sc.quiz_id = q.id
           WHERE c.subject_id = s.id) as avg_score
        FROM subject s;
    """)
    return db.session.execute(sql).fetchall()


def _send_email_plain(to_email, subject, body):
    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = to_email
    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as s:
        s.starttls()
        s.login(SMTP_USER, SMTP_PASS)
        s.sendmail(FROM_EMAIL, [to_email], msg.as_string())


@celery.task(bind=True, base=DatabaseTask, max_retries=3, default_retry_delay=60)
def send_subjects_stats_email(self, to_email):
    """
    Fetch subject stats and email them (plain text).
    Enqueued by the Flask endpoint; runs asynchronously on worker.
    """
    try:
        rows = _fetch_subject_stats()
        lines = ["Subject statistics:\n"]
        for r in rows:
            avg = f"{(float(r.avg_score) if r.avg_score is not None else 0):.2f}"
            lines.append(f"ID: {r.id}  Name: {r.name}  Users: {r.user_count or 0}  AvgScore: {avg}")
        body = "\n".join(lines)
        _send_email_plain(to_email, "Subject Stats Report", body)
        return {"status": "sent", "rows": len(rows)}
    except Exception as exc:
        logger.exception("send_subjects_stats_email failed")
        # retry with Celery retry policy
        raise self.retry(exc=exc)
