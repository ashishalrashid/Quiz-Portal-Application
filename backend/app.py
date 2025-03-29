from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource
from datetime import timedelta, date
from flask_cors import cross_origin
from sqlalchemy import text
import os
basedir = os.path.abspath(os.path.dirname(__file__))


basedir = os.path.abspath(os.path.dirname(__file__))
instance_path = os.path.abspath(os.path.join(basedir, "..", "instance"))

app = Flask(__name__, instance_relative_config=True, instance_path=instance_path)

try:
    os.makedirs(app.instance_path, exist_ok=True)
except OSError:
    pass

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)

app.config.from_mapping(
    CORS_HEADERS=['Content-Type', 'Authorization'],
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "db.sqlite3"),
    JWT_SECRET_KEY='super-secret',
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1)
)

db = SQLAlchemy()
api=Api(app)

jwt =JWTManager(app)
@jwt.invalid_token_loader
def invalid_token_callback(error_string):
    return jsonify({"msg": "Invalid token: " + error_string}), 422
db.init_app(app)

#make this intosperate file models.py in the future mabye?

class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    qualification = db.Column(db.String(32), nullable=False)
    dob = db.Column(db.Date, nullable=True)
    scores = db.relationship('Scores', backref='user', cascade="all, delete-orphan")
    usersubjects = db.relationship('UserSubject', backref='user', cascade="all, delete-orphan")
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())
    chapters = db.relationship('Chapter', backref='subject', cascade="all, delete-orphan")
    
    usersubjects = db.relationship('UserSubject', backref='subject', cascade="all, delete-orphan")

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', cascade="all, delete-orphan")

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    time_duration = db.Column(db.Interval, nullable=False, default=timedelta(minutes=20))
    scores = db.relationship('Scores', backref='quiz', cascade="all, delete-orphan")
    questions = db.relationship('Questions', backref='subject', cascade="all, delete-orphan")

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    score = db.Column(db.Integer)

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(), nullable=False)
    option1 = db.Column(db.String())
    option2 = db.Column(db.String())
    option3 = db.Column(db.String())
    option4 = db.Column(db.String())
    answer = db.Column(db.Integer, nullable=False)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)

class UserSubject(db.Model):
    __tablename__ = 'usersubject'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)



#milestone 0 completed
#milestone 1 completed 

with app.app_context():
    db.create_all()


class LoginResource(Resource):
    @cross_origin(origins="http://localhost:5173")
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=str(user.id)) 
            response = jsonify({"msg": "Successfully logged in", "token": access_token})
            return make_response(response, 200)
        response = jsonify({"msg": "Email or password incorrect."})
        return make_response(response, 401)

class AdminLoginResource(Resource):
    @cross_origin(origins="http://localhost:5173")
    def post(self):
        data = request.get_json()
        username = data['username'] 
        password = data['password']
        
        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password_hash(admin.password_hash, password):
            access_token = create_access_token(identity=admin.username)
            response = jsonify({"msg": "Admin login successful", "token": access_token})
            return make_response(response, 200)

        response = jsonify({"msg": "Invalid admin credentials."})
        return make_response(response, 401)
    
class Signup(Resource):
    @cross_origin(origins="http://localhost:5173")
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        name = data.get('name')
        qualification = data.get('qualification')
        dob_str = data.get('dob')
        dob = datetime.strptime(dob_str, "%Y-%m-%d").date() if dob_str else None
        user = User.query.filter_by(username=username).first()
        if user:
            return jsonify({'msg': 'User already exists'})
        new_user = User(username=username, email=email, full_name=name,
                        qualification=qualification, dob=dob)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'msg': 'User created successfully'})

########################################################           RBAC DONE              ###############################################################
########################################################        CRUD FOR   SUB            ###############################################################

class CreateSubject(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        if identity != "admin":
            return jsonify({"msg": "Only admin can create subjects"}), 403
        
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', None)
        if not name:
            return jsonify({"msg": "Subject name is required"}), 400
        
        subject = Subject(name=name, description=description)
        db.session.add(subject)
        db.session.commit()
        return jsonify({
            "msg": "Subject created successfully",
            "subject": {"id": subject.id, "name": subject.name, "description": subject.description}
        }), 201

class EditSubject(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def put(self, subject_id):
        identity = get_jwt_identity()
        if identity != "admin":
            return jsonify({"msg": "Only admin can edit subjects"}), 403
        data = request.get_json()
        subject = db.session.execute(
            db.text("SELECT * FROM subject WHERE id = :subject_id"),
            {"subject_id": subject_id}
        ).fetchone()
        if not subject:
            return jsonify({"msg": "Subject not found"}), 404
        db.session.execute(
            db.text("""
                UPDATE subject
                SET name = CASE WHEN :name = '' THEN name ELSE :name END,
                    description = CASE WHEN :description = '' THEN description ELSE :description END
                WHERE id = :subject_id
            """),
            {
                "name": data.get("name", ""),
                "description": data.get("description", ""),
                "subject_id": subject_id
            }
        )
        db.session.commit()
        updated_subject = db.session.execute(
            db.text("SELECT * FROM subject WHERE id = :subject_id"),
            {"subject_id": subject_id}
        ).fetchone()
        return jsonify({
            "msg": "Subject updated successfully",
            "subject": {
                "id": updated_subject.id,
                "name": updated_subject.name,
                "description": updated_subject.description
            }
        }), 200

class DeleteSubject(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def delete(self, subject_id):
        if get_jwt_identity() != "admin":
            return jsonify({"msg": "Only admin can delete subjects"}), 403
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({"msg": "Subject not found"}), 404
        db.session.delete(subject)
        db.session.commit()
        return jsonify({"msg": "Subject and related entries deleted successfully"}), 200

class GetSubject(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def get(self):
        subjects = Subject.query.all()
        subjects_data = [
            {"id": subject.id, "name": subject.name, "description": subject.description}
            for subject in subjects
        ]
        return jsonify({"subjects": subjects_data}), 200
########################################################        CRUD FOR SUBJECTS DONE        ###############################################################
########################################################        CRUD FOR   USERS              ###############################################################

class GetUsers(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def get(self):
        if get_jwt_identity() != "admin":
            return jsonify({"msg": "Only admin can view users"}), 403

        users = User.query.all()
        user_list = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "full_name": user.full_name,
                "qualification": user.qualification,
                "dob": user.dob.strftime("%Y-%m-%d") if user.dob else None
            }
            for user in users
        ]
        return jsonify(user_list)
    
class EditUser(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def put(self, user_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403

        data = request.get_json()
        if not isinstance(data, dict):
            return {"msg": "Invalid"}, 400

        user = db.session.execute(
            db.text("SELECT * FROM user WHERE id = :user_id"),
            {"user_id": user_id}
        ).fetchone()
        if not user:
            return {"msg": "User 404"}, 404

        username = data.get("username") if data.get("username") is not None else user.username
        email = data.get("email") if data.get("email") is not None else user.email
        full_name = data.get("full_name") if data.get("full_name") is not None else user.full_name
        qualification = data.get("qualification") if data.get("qualification") is not None else user.qualification
        dob_str = data.get("dob")
        if dob_str:
            try:
                dob = datetime.strptime(dob_str, "%Y-%m-%d").date()
            except ValueError:
                return {"msg": "Invalid date format. Use YYYY-MM-DD"}, 400
        else:
            dob = user.dob

        db.session.execute(
            db.text("""
                UPDATE user
                SET username = :username, email = :email, full_name = :full_name,
                    qualification = :qualification, dob = :dob
                WHERE id = :user_id
            """),
            {
                "username": username,
                "email": email,
                "full_name": full_name,
                "qualification": qualification,
                "dob": dob,
                "user_id": user_id
            }
        )
        db.session.commit()
        return {"msg": "User updated"}, 200

class DeleteUser(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def delete(self, user_id):
        if get_jwt_identity() != "admin":
            return jsonify({"msg": "Only admin can delete users"}), 403
        
        sql = text("DELETE FROM user WHERE id = :user_id")
        result = db.session.execute(sql, {"user_id": user_id})

        if result.rowcount == 0:
            return jsonify({"msg": "User not found"}), 404
        
        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200

########################################################        CRUD FOR users  DONE        ###############################################################
########################################################        CRUD FOR   CHAPTER          ###############################################################

class GetChapter(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def get(self, subject_id):
        chapters = db.session.execute(
            db.text("SELECT * FROM chapter WHERE subject_id = :subject_id"),
            {"subject_id": subject_id}
        ).fetchall()
        if not chapters:
            return {"msg": "No chapters found"}, 404
        chapters_list = [dict(ch._mapping) for ch in chapters]
        return {"chapters": chapters_list}, 200

class CreateChapter(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def post(self, subject_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403
        data = request.get_json()
        if not isinstance(data, dict):
            return {"msg": "Invalid data format"}, 400
        name = data.get("name")
        description = data.get("description", "")
        if not name:
            return {"msg": "Chapter name is required"}, 400
        db.session.execute(
            db.text("INSERT INTO chapter (name, description, subject_id) VALUES (:name, :description, :subject_id)"),
            {"name": name, "description": description, "subject_id": subject_id}
        )
        db.session.commit()
        return {"msg": "Chapter created successfully"}, 201

class EditChapter(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def put(self, chapter_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403
        data = request.get_json()
        if not isinstance(data, dict):
            return {"msg": "Invalid data format"}, 400
        chapter = db.session.execute(
            db.text("SELECT * FROM chapter WHERE id = :chapter_id"),
            {"chapter_id": chapter_id}
        ).fetchone()
        if not chapter:
            return {"msg": "Chapter not found"}, 404
        name = data.get("name", chapter.name)
        description = data.get("description", chapter.description)
        db.session.execute(
            db.text("UPDATE chapter SET name = :name, description = :description WHERE id = :chapter_id"),
            {"name": name, "description": description, "chapter_id": chapter_id}
        )
        db.session.commit()
        return {"msg": "Chapter updated successfully"}, 200

class DeleteChapter(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def delete(self, chapter_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403
        chapter = db.session.execute(
            db.text("SELECT * FROM chapter WHERE id = :chapter_id"),
            {"chapter_id": chapter_id}
        ).fetchone()
        if not chapter:
            return {"msg": "Chapter not found"}, 404
        db.session.execute(
            db.text("DELETE FROM chapter WHERE id = :chapter_id"),
            {"chapter_id": chapter_id}
        )
        db.session.commit()
        return {"msg": "Chapter deleted successfully"}, 200

########################################################        CRUD FOR CHAPTER  DONE        ###############################################################
########################################################           CRUD FOR   Quiz             ###############################################################

class GetQuiz(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def get(self, chapter_id):
        quizzes = db.session.execute(
            db.text("""
                SELECT id, name, chapter_id, start_date, end_date, time_duration 
                FROM quiz
                WHERE chapter_id = :chapter_id
            """),
            {"chapter_id": chapter_id}
        ).fetchall()
        
        if not quizzes:
            return {"msg": "No quizzes found"}, 404
        
        quizzes_list = []
        base = datetime(1970, 1, 1)
        for q in quizzes:
            q_dict = dict(q._mapping)
            if isinstance(q_dict["time_duration"], str):
                dt = datetime.strptime(q_dict["time_duration"], "%Y-%m-%d %H:%M:%S.%f")
                q_dict["time_duration"] = int((dt - base).total_seconds() // 60)
            elif hasattr(q_dict["time_duration"], "total_seconds"):
                q_dict["time_duration"] = int(q_dict["time_duration"].total_seconds() // 60)
            else:
                q_dict["time_duration"] = int(q_dict["time_duration"])
            quizzes_list.append(q_dict)

        return {"quizzes": quizzes_list}, 200

class CreateQuiz(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def post(self, chapter_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403
        data = request.get_json()
        if not isinstance(data, dict):
            return {"msg": "Invalid data format"}, 400
        name = data.get("name")
        if not name:
            return {"msg": "Quiz name is required"}, 400
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        time_duration_minutes = data.get("time_duration")
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else None
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else None
            time_duration = int(float(time_duration_minutes)) if time_duration_minutes is not None else 20
        except Exception:
            return {"msg": "Invalid date or duration format"}, 400
        db.session.execute(
            db.text("INSERT INTO quiz (name, chapter_id, start_date, end_date, time_duration) VALUES (:name, :chapter_id, :start_date, :end_date, :time_duration)"),
            {"name": name, "chapter_id": chapter_id, "start_date": start_date, "end_date": end_date, "time_duration": time_duration}
        )
        db.session.commit()
        return {"msg": "Quiz created successfully"}, 201

class EditQuiz(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def put(self, quiz_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403

        data = request.get_json()
        if not isinstance(data, dict):
            return {"msg": "Invalid data format"}, 400

        quiz = db.session.execute(
            db.text("SELECT * FROM quiz WHERE id = :quiz_id"),
            {"quiz_id": quiz_id}
        ).fetchone()
        if not quiz:
            return {"msg": "Quiz not found"}, 404

        name = data.get("name", quiz.name)
        chapter_id = data.get("chapter_id", quiz.chapter_id)
        start_date_str = data.get("start_date")
        end_date_str = data.get("end_date")
        time_duration_input = data.get("time_duration")

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d").date() if start_date_str else quiz.start_date
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d").date() if end_date_str else quiz.end_date
            if time_duration_input is not None:
                time_duration = int(float(time_duration_input))
            else:
                if hasattr(quiz.time_duration, "total_seconds"):
                    time_duration = int(quiz.time_duration.total_seconds() // 60)
                else:
                    time_duration = quiz.time_duration
        except Exception:
            return {"msg": "Invalid date or duration format"}, 400

        # Build update query dynamically
        update_fields = [
            "name = :name",
            "start_date = :start_date",
            "end_date = :end_date",
            "time_duration = :time_duration"
        ]
        params = {
            "name": name,
            "start_date": start_date,
            "end_date": end_date,
            "time_duration": time_duration,
            "quiz_id": quiz_id
        }
        query = f"UPDATE quiz SET {', '.join(update_fields)} WHERE id = :quiz_id"
        db.session.execute(db.text(query), params)
        db.session.commit()

        return {"msg": "Quiz updated successfully"}, 200

class DeleteQuiz(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def delete(self, quiz_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403
        quiz = db.session.execute(
            db.text("SELECT * FROM quiz WHERE id = :quiz_id"),
            {"quiz_id": quiz_id}
        ).fetchone()
        if not quiz:
            return {"msg": "Quiz not found"}, 404
        db.session.execute(
            db.text("DELETE FROM quiz WHERE id = :quiz_id"),
            {"quiz_id": quiz_id}
        )
        db.session.commit()
        return {"msg": "Quiz deleted successfully"}, 200

########################################################             CRUD FOR QUIZ DONE               ###############################################################
########################################################            CRUD FOR QUESTIONS                ###############################################################

class EditQuestion(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def put(self, question_id):
        if get_jwt_identity() != "admin":
            return {"msg": "Not authorized"}, 403
        data = request.get_json()
        if not isinstance(data, dict):
            return {"msg": "Invalid data format"}, 400
        question = db.session.execute(
            db.text("SELECT * FROM questions WHERE id = :question_id"),
            {"question_id": question_id}
        ).fetchone()
        if not question:
            return {"msg": "Question not found"}, 404
        question_text = data.get("question", question.question)
        option1 = data.get("option1", question.option1)
        option2 = data.get("option2", question.option2)
        option3 = data.get("option3", question.option3)
        option4 = data.get("option4", question.option4)
        answer = data.get("answer", question.answer)
        db.session.execute(
            db.text("""
                UPDATE questions
                SET question = :question, option1 = :option1, option2 = :option2,
                    option3 = :option3, option4 = :option4, answer = :answer
                WHERE id = :question_id
            """),
            {
                "question": question_text,
                "option1": option1,
                "option2": option2,
                "option3": option3,
                "option4": option4,
                "answer": answer,
                "question_id": question_id
            }
        )
        db.session.commit()
        return {"msg": "Question updated"}, 200

class DeleteQuestion(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def delete(self, question_id):
        if get_jwt_identity() != "admin":
            return {"msg": "Not authorized"}, 403
        db.session.execute(
            db.text("DELETE FROM questions WHERE id = :question_id"),
            {"question_id": question_id}
        )
        db.session.commit()
        return {"msg": "Question deleted"}, 200

class GetQuestions(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def get(self, quiz_id):
        questions = db.session.execute(
            db.text("""
                SELECT q.id, q.question, q.option1, q.option2, q.option3, q.option4, q.answer
                FROM questions q
                WHERE q.quiz_id = :quiz_id
            """),
            {"quiz_id": quiz_id}
        ).fetchall()
        return [{
            "id": q.id,
            "question": q.question,
            "options": [q.option1, q.option2, q.option3, q.option4],
            "answer": q.answer
        } for q in questions], 200

class CreateQuestion(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def post(self, quiz_id):
        if get_jwt_identity() != "admin":
            return {"msg": "Not authorized"}, 403
        data = request.get_json()
        if not isinstance(data, dict):
            return {"msg": "Invalid data format"}, 400
        question_text = data.get("question")
        option1 = data.get("option1")
        option2 = data.get("option2")
        option3 = data.get("option3")
        option4 = data.get("option4")
        answer = data.get("answer")
        if not all([question_text, option1, option2, option3, option4, answer]):
            return {"msg": "Missing required fields"}, 400
        db.session.execute(
            db.text("""
                INSERT INTO questions (question, option1, option2, option3, option4, answer, quiz_id)
                VALUES (:question, :option1, :option2, :option3, :option4, :answer, :quiz_id)
            """),
            {
                "question": question_text,
                "option1": option1,
                "option2": option2,
                "option3": option3,
                "option4": option4,
                "answer": answer,
                "quiz_id": quiz_id
            }
        )
        db.session.commit()
        return {"msg": "Question created successfully"}, 201

########################################################             ADMIN DONE               ###############################################################
##################################         USERS: TAKE QUESTIONS, EVALUATE QUESTIONS, GET SUB CHAPTERS,AND QUIZ            ##############################################
class GetUserSubjects(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def get(self):
        user_id = get_jwt_identity()

        sql = text("""
            SELECT s.id AS id, COALESCE(CAST(s.name AS TEXT), 'nosub') AS name
            FROM usersubject AS us
            JOIN subject AS s ON s.id = us.subject_id
            WHERE us.user_id = :user_id
        """)

        result = db.session.execute(sql, {"user_id": user_id}).fetchall()

        subjects = [{"id": row.id, "name": row.name} for row in result]
        return jsonify({"subjects": subjects})

class GetUserQuizzes(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def get(self,subject_id):
        today = date.today()
        sql = text("""
            SELECT q.id, q.name AS quiz_name, c.name AS chapter_name,
                   q.start_date, q.end_date, q.time_duration
            FROM quiz q
            JOIN chapter c ON q.chapter_id = c.id
            WHERE q.end_date >= :today
                   and c.subject_id=:subject_id
                   and q.start_date <= :today
        """)
        result = db.session.execute(sql, {"subject_id": subject_id, "today": today}).fetchall()
        quizzes = []
        for row in result:
            duration = None
            if row.time_duration:
                try:
                    duration = int(row.time_duration.total_seconds() // 60)
                except Exception:
                    duration = row.time_duration
            quizzes.append({
                "id": row.id,
                "quiz_name": row.quiz_name,
                "chapter_name": row.chapter_name,
                "start_date":  row.start_date ,
                "end_date": row.end_date ,
                "duration": duration
            })
        return jsonify({"quizzes": quizzes})

class CreateUserSubject(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def post(self, subject_id):
        user_id = get_jwt_identity()
        check_sql = text("""
            SELECT id FROM usersubject
            WHERE subject_id = :subject_id AND user_id = :user_id
        """)
        existing = db.session.execute(check_sql, {"subject_id": subject_id, "user_id": user_id}).fetchone()
        if existing:
            return jsonify({"msg": "UserSubject already exists"}), 200
        sql = text("""
            INSERT INTO usersubject (subject_id, user_id)
            VALUES (:subject_id, :user_id)
        """)
        db.session.execute(sql, {"subject_id": subject_id, "user_id": user_id})
        db.session.commit()
        return jsonify({"msg": "UserSubject created successfully"}), 201

class GetOtherSubjects(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        sql = text("""
            SELECT s.id, s.name, s.description
            FROM subject s
            WHERE s.id NOT IN (
                SELECT us.subject_id
                FROM usersubject us
                WHERE us.user_id = :user_id
            )
        """)
        result = db.session.execute(sql, {"user_id": user_id}).fetchall()
        subjects_data = [
            {"id": row.id, "name": row.name, "description": row.description}
            for row in result
        ]
        return jsonify({"subjects": subjects_data}), 200


########################################################             CRUD  DONE               ###############################################################
########################################################             STATS CALC                ###############################################################

class GetCounts(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def get(self):
        user_result = db.session.execute(text("SELECT COUNT(*) as count FROM user")).fetchone()
        user_count = user_result[0] if user_result else 0

        quiz_result = db.session.execute(text("SELECT COUNT(*) as count FROM quiz")).fetchone()
        quiz_count = quiz_result[0] if quiz_result else 0

        subject_result = db.session.execute(text("SELECT COUNT(*) as count FROM subject")).fetchone()
        subject_count = subject_result[0] if subject_result else 0

        chapter_result = db.session.execute(text("SELECT COUNT(*) as count FROM chapter")).fetchone()
        chapter_count = chapter_result[0] if chapter_result else 0

        return {
            "user_count": user_count,
            "quiz_count": quiz_count,
            "subject_count": subject_count,
            "chapter_count": chapter_count
        }, 200

class SubjectStats(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def get(self):
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
        result = db.session.execute(sql).fetchall()
        stats = [{
            "id": row.id,
            "name": row.name,
            "user_count": row.user_count,
            "avg_score": row.avg_score
        } for row in result]
        return jsonify({"stats": stats})

########################################################             STATS DONE               ###############################################################
########################################################             RESOURCES                ###############################################################

api.add_resource(LoginResource, '/login')
api.add_resource(Signup, '/signup')
api.add_resource(AdminLoginResource, '/adminlogin')
api.add_resource(CreateSubject,'/createsubject')
api.add_resource(EditSubject, '/editsubject/<int:subject_id>')
api.add_resource(DeleteSubject,'/deletesubject/<int:subject_id>')
api.add_resource(GetSubject, "/getsubjects")
api.add_resource(GetUsers, "/getusers")
api.add_resource(EditUser, "/edituser/<int:user_id>")
api.add_resource(DeleteUser, "/deleteuser/<int:user_id>")
api.add_resource(GetChapter, "/getchapter/<int:subject_id>")
api.add_resource(CreateChapter, "/createchapter/<int:subject_id>")
api.add_resource(EditChapter, "/editchapter/<int:chapter_id>")
api.add_resource(DeleteChapter, "/deletechapter/<int:chapter_id>")
api.add_resource(CreateQuiz,"/createquiz/<int:chapter_id>")
api.add_resource(GetQuiz,"/getquiz/<int:chapter_id>")
api.add_resource(DeleteQuiz,"/deletequiz/<int:quiz_id>")
api.add_resource(EditQuiz,"/editquiz/<int:quiz_id>")
api.add_resource(CreateQuestion, "/createquestion/<int:quiz_id>")
api.add_resource(EditQuestion, "/editquestion/<int:question_id>")
api.add_resource(DeleteQuestion, "/deletequestion/<int:question_id>")
api.add_resource(GetQuestions,"/getquestion/<int:quiz_id>")
api.add_resource(GetCounts,"/getcounts")
api.add_resource(SubjectStats,"/subjectstats")
api.add_resource(GetUserSubjects,"/getus")
api.add_resource(GetUserQuizzes,"/getuserquizzes/<int:subject_id>")
api.add_resource(CreateUserSubject,"/createusersubject/<int:subject_id>")
api.add_resource(GetOtherSubjects,"/getothersubjects")

if __name__ == '__main__':
    app.run(debug=True)