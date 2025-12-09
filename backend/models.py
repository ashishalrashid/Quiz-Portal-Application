from datetime import timedelta

from werkzeug.security import generate_password_hash, check_password_hash

from extensions import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    qualification = db.Column(db.String(32), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    scores = db.relationship("Scores", backref="user", cascade="all, delete-orphan")
    usersubjects = db.relationship("UserSubject", backref="user", cascade="all, delete-orphan")

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())
    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete-orphan")
    usersubjects = db.relationship("UserSubject", backref="subject", cascade="all, delete-orphan")


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id", ondelete="CASCADE"), nullable=False)
    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete-orphan")


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id", ondelete="CASCADE"), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    time_duration = db.Column(db.Interval, nullable=False, default=timedelta(minutes=20))
    scores = db.relationship("Scores", backref="quiz", cascade="all, delete-orphan")
    questions = db.relationship("Questions", backref="subject", cascade="all, delete-orphan")


class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    score = db.Column(db.Integer)


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(), nullable=False)
    option1 = db.Column(db.String())
    option2 = db.Column(db.String())
    option3 = db.Column(db.String())
    option4 = db.Column(db.String())
    answer = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id", ondelete="CASCADE"), nullable=False)


class UserSubject(db.Model):
    __tablename__ = "usersubject"
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

