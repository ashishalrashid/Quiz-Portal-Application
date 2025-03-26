from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource
from datetime import timedelta
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

app.config.from_mapping(
    CORS_HEADERS=['Content-Type', 'Authorization'],
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, "db.sqlite3"),
    JWT_SECRET_KEY='super-secret',
    JWT_ACCESS_TOKEN_EXPIRES=timedelta(days=1)
)

db = SQLAlchemy()
api=Api(app)
CORS(app)
jwt =JWTManager(app)

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
    user_subjects = db.relationship('User_Subject', backref='user', cascade="all, delete-orphan")
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String())
    chapters = db.relationship('Chapter', backref='subject', cascade="all, delete-orphan")
    questions = db.relationship('Questions', backref='subject', cascade="all, delete-orphan")
    user_subjects = db.relationship('User_Subject', backref='subject', cascade="all, delete-orphan")

class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String())
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    quizzes = db.relationship('Quiz', backref='chapter', cascade="all, delete-orphan")

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('chapter.id', ondelete='CASCADE'), nullable=False)
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)
    time_duration = db.Column(db.Interval, nullable=False, default=timedelta(minutes=20))
    scores = db.relationship('Scores', backref='quiz', cascade="all, delete-orphan")
    question_quizzes = db.relationship('Question_Quiz', backref='quiz', cascade="all, delete-orphan")

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
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    question_quizzes = db.relationship('Question_Quiz', backref='question', cascade="all, delete-orphan")

class User_Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id', ondelete='CASCADE'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

class Question_Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id', ondelete='CASCADE'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id', ondelete='CASCADE'), nullable=False)


#milestone 0 completed
#milestone 1 completed 

with app.app_context():
    db.create_all()

class Hello(Resource):
    @cross_origin()
    @jwt_required()
    def get(self):
        username=get_jwt_identity()
        return jsonify({'msg':"Hello world","username":username})
    
class LoginResource(Resource):
    def post(self):
        data = request.get_json()
        email = data['email']
        password = data['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            response = jsonify({"msg":"successfully logged in", "token": access_token})
            return make_response(response, 401)
        response = jsonify({"msg": "email or password incorrect."})
        return make_response(response, 200)

class AdminLoginResource(Resource):
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
    @cross_origin()
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
    
class CreateSubject(Resource):
    @cross_origin()
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
    @cross_origin()
    @jwt_required()
    def put(self, subject_id):
        identity = get_jwt_identity()
        if identity != "admin":
            return jsonify({"msg": "Only admin can edit subjects"}), 403
        data = request.get_json()
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({"msg": "Subject not found"}), 404
        name = data.get('name')
        description = data.get('description', None)
        if name:
            subject.name = name
        subject.description = description
        db.session.commit()
        return jsonify({
            "msg": "Subject updated successfully",
            "subject": {"id": subject.id, "name": subject.name, "description": subject.description}
        }), 200

class DeleteSubject(Resource):
    @cross_origin()
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
    @cross_origin()
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
    @cross_origin()
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
    def get(self, subject_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403
        chapters = db.session.execute(
            db.text("SELECT * FROM chapter WHERE subject_id = :subject_id"),
            {"subject_id": subject_id}
        ).fetchall()
        if not chapters:
            return {"msg": "No chapters found"}, 404
        chapters_list = [dict(ch._mapping) for ch in chapters]
        return {"chapters": chapters_list}, 200

class CreateChapter(Resource):
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

class GetQuestions(Resource):
    @jwt_required()
    def get(self, quiz_id):
        questions = db.session.execute(
            db.text("""
                SELECT q.id, q.question, q.option1, q.option2, q.option3, q.option4, q.answer, q.subject_id
                FROM questions q
                JOIN question_quiz qq ON q.id = qq.question_id
                WHERE qq.quiz_id = :quiz_id
            """),
            {"quiz_id": quiz_id}
        ).fetchall()

        return [{
            "id": q.id, "question": q.question,
            "options": [q.option1, q.option2, q.option3, q.option4],
            "answer": q.answer, "subject_id": q.subject_id
        } for q in questions], 200


class CreateQuestion(Resource):
    @jwt_required()
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
        subject_id = data.get("subject_id")

        if not all([question_text, option1, option2, option3, option4, answer, subject_id]):
            return {"msg": "Missing required fields"}, 400

        db.session.execute(
            db.text("""
                INSERT INTO questions (question, option1, option2, option3, option4, answer, subject_id)
                VALUES (:question, :option1, :option2, :option3, :option4, :answer, :subject_id)
            """),
            {
                "question": question_text,
                "option1": option1,
                "option2": option2,
                "option3": option3,
                "option4": option4,
                "answer": answer,
                "subject_id": subject_id
            }
        )
        db.session.commit()

        return {"msg": "Question created successfully"}, 201


class UpdateQuestion(Resource):
    @jwt_required()
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
    def delete(self, question_id):
        if get_jwt_identity() != "admin":
            return {"msg": "Not authorized"}, 403

        db.session.execute(
            db.text("DELETE FROM questions WHERE id = :question_id"),
            {"question_id": question_id}
        )
        db.session.commit()
        return {"msg": "Question deleted"}, 200

########################################################             CRUD FOR QUIZ DONE               ###############################################################
########################################################            CRUD FOR QUESTIONS                ###############################################################

class CreateQuestion(Resource):
    @jwt_required()
    def post(self, quiz_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403

        data = request.get_json()
        if not isinstance(data, dict):
            return {"msg": "Invalid data format"}, 400

        question_text = data.get("question_text")
        options = data.get("options")
        correct_option = data.get("correct_option")
        marks = data.get("marks", 1)

        if not question_text or not options or correct_option not in options:
            return {"msg": "Invalid question data"}, 400

        db.session.execute(
            db.text("""
                INSERT INTO questions (quiz_id, question_text, options, correct_option, marks)
                VALUES (:quiz_id, :question_text, :options, :correct_option, :marks)
            """),
            {
                "quiz_id": quiz_id,
                "question_text": question_text,
                "options": json.dumps(options),
                "correct_option": correct_option,
                "marks": marks
            }
        )
        db.session.commit()
        return {"msg": "Question created successfully"}, 201


class ReadQuestions(Resource):
    @jwt_required()
    def get(self, quiz_id):
        questions = db.session.execute(
            db.text("SELECT * FROM questions WHERE quiz_id = :quiz_id"),
            {"quiz_id": quiz_id}
        ).fetchall()

        return [{"id": q.id, "question_text": q.question_text, "options": json.loads(q.options),
                 "correct_option": q.correct_option, "marks": q.marks} for q in questions], 200


class UpdateQuestion(Resource):
    @jwt_required()
    def put(self, question_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403

        data = request.get_json()
        if not isinstance(data, dict):
            return {"msg": "Invalid"}, 400

        question = db.session.execute(
            db.text("SELECT * FROM questions WHERE id = :question_id"),
            {"question_id": question_id}
        ).fetchone()
        if not question:
            return {"msg": "Question not found"}, 404

        question_text = data.get("question_text", question.question_text)
        options = data.get("options", json.loads(question.options))
        correct_option = data.get("correct_option", question.correct_option)
        marks = data.get("marks", question.marks)

        if correct_option not in options:
            return {"msg": "Invalid correct option"}, 400

        db.session.execute(
            db.text("""
                UPDATE questions
                SET question_text = :question_text, options = :options,
                    correct_option = :correct_option, marks = :marks
                WHERE id = :question_id
            """),
            {
                "question_text": question_text,
                "options": json.dumps(options),
                "correct_option": correct_option,
                "marks": marks,
                "question_id": question_id
            }
        )
        db.session.commit()
        return {"msg": "Question updated"}, 200


class DeleteQuestion(Resource):
    @jwt_required()
    def delete(self, question_id):
        if get_jwt_identity() != "admin":
            return {"msg": "not admin"}, 403

        db.session.execute(
            db.text("DELETE FROM questions WHERE id = :question_id"),
            {"question_id": question_id}
        )
        db.session.commit()
        return {"msg": "Question deleted"}, 200


########################################################             CRUD  DONE               ###############################################################
########################################################             RESOURCES                ###############################################################

api.add_resource(Hello, '/hello')
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


if __name__ == '__main__':
    app.run(debug=True)