import os
from datetime import date, timedelta
from app import app, db, Admin, User, Subject, Chapter, Quiz, Scores, Questions, User_Subject, Question_Quiz

# Configure the database URI to use the instance folder (same as defined in your main app)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(app.instance_path, "db.sqlite3")

with app.app_context():
    # Drop all tables and recreate them
    db.drop_all()
    db.create_all()

    # Create admin user
    admin = Admin(username="admin")
    admin.set_password("adminpass")
    db.session.add(admin)

    # Create multiple users
    user1 = User(username="testuser", email="testuser@example.com", full_name="Test User", qualification="B.Tech", dob=date(1995, 5, 15))
    user1.set_password("userpass")
    db.session.add(user1)
    user2 = User(username="johndoe", email="john@example.com", full_name="John Doe", qualification="M.Sc", dob=date(1990, 2, 10))
    user2.set_password("doepass")
    db.session.add(user2)
    user3 = User(username="janedoe", email="jane@example.com", full_name="Jane Doe", qualification="Ph.D", dob=date(1988, 7, 22))
    user3.set_password("janepass")
    db.session.add(user3)

    # Create subjects
    subject1 = Subject(name="Mathematics", description="All about numbers and equations.")
    subject2 = Subject(name="Physics", description="The study of matter and energy.")
    db.session.add(subject1)
    db.session.add(subject2)
    db.session.flush()  # Ensure subject IDs are generated

    # Create chapters (new table) for subdividing subjects
    chapter1 = Chapter(name="Algebra", description="Basics of algebra", subject_id=subject1.id)
    chapter2 = Chapter(name="Geometry", description="Basics of geometry", subject_id=subject1.id)
    chapter3 = Chapter(name="Mechanics", description="Motion and forces", subject_id=subject2.id)
    chapter4 = Chapter(name="Optics", description="Light and vision", subject_id=subject2.id)
    db.session.add(chapter1)
    db.session.add(chapter2)
    db.session.add(chapter3)
    db.session.add(chapter4)
    db.session.flush()  # Ensure chapter IDs are generated

    # Create quizzes - Note: Quiz now refers to a chapter (chapter_id) instead of subject
    quiz1 = Quiz(chapter_id=chapter1.id, start_date=date(2025, 1, 1), end_date=date(2025, 1, 10), time_duration=timedelta(minutes=30))
    quiz2 = Quiz(chapter_id=chapter2.id, start_date=date(2025, 2, 1), end_date=date(2025, 2, 10), time_duration=timedelta(minutes=25))
    quiz3 = Quiz(chapter_id=chapter3.id, start_date=date(2025, 3, 1), end_date=date(2025, 3, 10), time_duration=timedelta(minutes=35))
    quiz4 = Quiz(chapter_id=chapter4.id, start_date=date(2025, 4, 1), end_date=date(2025, 4, 10), time_duration=timedelta(minutes=40))
    db.session.add(quiz1)
    db.session.add(quiz2)
    db.session.add(quiz3)
    db.session.add(quiz4)
    db.session.flush()  # Ensure quiz IDs are generated

    # Create questions
    q1 = Questions(question="What is 2+2?", option1="3", option2="4", option3="5", option4="22", answer=2, subject_id=subject1.id)
    q2 = Questions(question="Solve 2x=10", option1="4", option2="5", option3="6", option4="7", answer=2, subject_id=subject1.id)
    q3 = Questions(question="What is Newton's second law?", option1="F=ma", option2="E=mc^2", option3="a^2+b^2=c^2", option4="V=IR", answer=1, subject_id=subject2.id)
    q4 = Questions(question="What is the speed of light?", option1="3x10^8 m/s", option2="1x10^8 m/s", option3="2x10^8 m/s", option4="5x10^8 m/s", answer=1, subject_id=subject2.id)
    db.session.add(q1)
    db.session.add(q2)
    db.session.add(q3)
    db.session.add(q4)
    db.session.flush()  # Ensure question IDs are generated

    # Create scores for quizzes
    score1 = Scores(quiz_id=quiz1.id, user_id=user1.id, score=85)
    score2 = Scores(quiz_id=quiz2.id, user_id=user2.id, score=90)
    score3 = Scores(quiz_id=quiz3.id, user_id=user3.id, score=75)
    db.session.add(score1)
    db.session.add(score2)
    db.session.add(score3)

    # Create user_subject relationships
    us1 = User_Subject(subject_id=subject1.id, user_id=user1.id)
    us2 = User_Subject(subject_id=subject1.id, user_id=user2.id)
    us3 = User_Subject(subject_id=subject2.id, user_id=user3.id)
    db.session.add(us1)
    db.session.add(us2)
    db.session.add(us3)

    # Map questions to quizzes via Question_Quiz table
    qq1 = Question_Quiz(quiz_id=quiz1.id, question_id=q1.id)
    qq2 = Question_Quiz(quiz_id=quiz1.id, question_id=q2.id)
    qq3 = Question_Quiz(quiz_id=quiz3.id, question_id=q3.id)
    qq4 = Question_Quiz(quiz_id=quiz3.id, question_id=q4.id)
    db.session.add(qq1)
    db.session.add(qq2)
    db.session.add(qq3)
    db.session.add(qq4)

    db.session.commit()
    print("Sample data added successfully!")
