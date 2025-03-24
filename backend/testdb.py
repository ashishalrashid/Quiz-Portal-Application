import os
from datetime import date, timedelta
from app import app, db, Admin, User, Subject, Quiz, Scores, Questions, User_Subject, Question_Quiz

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.instance_path, "db.sqlite3")

with app.app_context():
    db.drop_all()
    db.create_all()

    admin = Admin(username="admin")
    admin.set_password("adminpass")
    db.session.add(admin)

    user = User(
        username="testuser",
        email="testuser@example.com",
        full_name="Test User",
        qualification="B.Tech",
        dob=date(1995, 5, 15)
    )
    user.set_password("userpass")
    db.session.add(user)

    subject = Subject(
        name="Mathematics",
        description="All about numbers and equations."
    )
    db.session.add(subject)
    db.session.flush()  # to get subject.id

    quiz = Quiz(
        subject_id=subject.id,
        start_date=date(2025, 1, 1),
        end_date=date(2025, 1, 10),
        time_duration=timedelta(minutes=30)
    )
    db.session.add(quiz)
    db.session.flush()  # to get quiz.id

    question = Questions(
        question="What is 2+2?",
        option1="3",
        option2="4",
        option3="5",
        option4="22",
        answer=2,
        subject_id=subject.id
    )
    db.session.add(question)
    db.session.flush()  # to get question.id

    score = Scores(
        quiz_id=quiz.id,
        user_id=user.id,
        score=100
    )
    db.session.add(score)

    user_subject = User_Subject(
        subject_id=subject.id,
        user_id=user.id
    )
    db.session.add(user_subject)

    question_quiz = Question_Quiz(
        quiz_id=quiz.id,
        question_id=question.id
    )
    db.session.add(question_quiz)

    db.session.commit()
    print("Sample data added successfully!")
