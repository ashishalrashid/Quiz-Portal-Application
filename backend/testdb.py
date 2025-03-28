import os
from datetime import date, timedelta
from app import app, db, Admin, User, Subject, Chapter, Quiz, Scores, Questions, User_Subject

# Configure the database URI to use the instance folder
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
    users = [
        User(username="testuser", email="testuser@example.com", full_name="Test User", qualification="B.Tech", dob=date(1995, 5, 15)),
        User(username="johndoe", email="john@example.com", full_name="John Doe", qualification="M.Sc", dob=date(1990, 2, 10)),
        User(username="janedoe", email="jane@example.com", full_name="Jane Doe", qualification="Ph.D", dob=date(1988, 7, 22)),
        User(username="alice123", email="alice@example.com", full_name="Alice Brown", qualification="B.Sc", dob=date(1999, 11, 5)),
        User(username="bob99", email="bob@example.com", full_name="Bob Smith", qualification="M.Tech", dob=date(1993, 4, 25)),
    ]
    for user in users:
        user.set_password("password123")
        db.session.add(user)
    
    db.session.flush()

    # Create subjects
    subjects = [
        Subject(name="Mathematics", description="All about numbers and equations."),
        Subject(name="Physics", description="The study of matter and energy."),
        Subject(name="Computer Science", description="Programming and algorithms."),
    ]
    db.session.add_all(subjects)
    db.session.flush()

    # Create chapters
    chapters = [
        Chapter(name="Algebra", description="Basics of algebra", subject_id=subjects[0].id),
        Chapter(name="Geometry", description="Basics of geometry", subject_id=subjects[0].id),
        Chapter(name="Mechanics", description="Motion and forces", subject_id=subjects[1].id),
        Chapter(name="Optics", description="Light and vision", subject_id=subjects[1].id),
        Chapter(name="Data Structures", description="Introduction to data structures", subject_id=subjects[2].id),
        Chapter(name="Algorithms", description="Understanding algorithms", subject_id=subjects[2].id),
    ]
    db.session.add_all(chapters)
    db.session.flush()

    # Create quizzes
    quizzes = [
        Quiz(name="Algebra Quiz 1", chapter_id=chapters[0].id, start_date=date(2025, 1, 1), end_date=date(2025, 1, 10), time_duration=timedelta(minutes=30)),
        Quiz(name="Geometry Quiz 1", chapter_id=chapters[1].id, start_date=date(2025, 2, 1), end_date=date(2025, 2, 10), time_duration=timedelta(minutes=25)),
        Quiz(name="Mechanics Quiz 1", chapter_id=chapters[2].id, start_date=date(2025, 3, 1), end_date=date(2025, 3, 10), time_duration=timedelta(minutes=35)),
        Quiz(name="Optics Quiz 1", chapter_id=chapters[3].id, start_date=date(2025, 4, 1), end_date=date(2025, 4, 10), time_duration=timedelta(minutes=40)),
        Quiz(name="Data Structures Quiz 1", chapter_id=chapters[4].id, start_date=date(2025, 5, 1), end_date=date(2025, 5, 10), time_duration=timedelta(minutes=30)),
        Quiz(name="Algorithms Quiz 1", chapter_id=chapters[5].id, start_date=date(2025, 6, 1), end_date=date(2025, 6, 10), time_duration=timedelta(minutes=45)),
    ]
    db.session.add_all(quizzes)
    db.session.flush()

    # Create questions (using quiz_id instead of subject_id)
    questions = [
        Questions(question="What is 2+2?", option1="3", option2="4", option3="5", option4="22", answer=2, quiz_id=quizzes[0].id),
        Questions(question="Solve 2x=10", option1="4", option2="5", option3="6", option4="7", answer=2, quiz_id=quizzes[0].id),
        Questions(question="What is Newton's second law?", option1="F=ma", option2="E=mc^2", option3="a^2+b^2=c^2", option4="V=IR", answer=1, quiz_id=quizzes[2].id),
        Questions(question="What is the speed of light?", option1="3x10^8 m/s", option2="1x10^8 m/s", option3="2x10^8 m/s", option4="5x10^8 m/s", answer=1, quiz_id=quizzes[3].id),
        Questions(question="Which data structure is LIFO?", option1="Queue", option2="Stack", option3="Heap", option4="Linked List", answer=2, quiz_id=quizzes[4].id),
        Questions(question="What is the time complexity of binary search?", option1="O(n)", option2="O(n log n)", option3="O(log n)", option4="O(1)", answer=3, quiz_id=quizzes[5].id),
    ]
    db.session.add_all(questions)
    db.session.flush()

    # Create scores
    scores = [
        Scores(quiz_id=quizzes[0].id, user_id=users[0].id, score=85),
        Scores(quiz_id=quizzes[1].id, user_id=users[1].id, score=90),
        Scores(quiz_id=quizzes[2].id, user_id=users[2].id, score=75),
        Scores(quiz_id=quizzes[3].id, user_id=users[3].id, score=80),
        Scores(quiz_id=quizzes[4].id, user_id=users[4].id, score=88),
        Scores(quiz_id=quizzes[5].id, user_id=users[0].id, score=92),
    ]
    db.session.add_all(scores)

    db.session.commit()
    print("Sample data added successfully!")
