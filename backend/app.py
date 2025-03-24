from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_restful import Api, Resource
from datetime import timedelta
from flask_cors import cross_origin
import os
basedir = os.path.abspath(os.path.dirname(__file__))

import os
from datetime import timedelta
from flask import Flask

app = Flask(__name__, instance_relative_config=True)

try:
    os.makedirs(app.instance_path)
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
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta, date



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

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=False)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False) 
    start_date = db.Column(db.Date, nullable=True)
    end_date = db.Column(db.Date, nullable=True)  # Deadline
    time_duration = db.Column(db.Interval, nullable=False, default=timedelta(minutes=20))

class Scores(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) 
    score = db.Column(db.Integer)  

class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(), nullable=False)
    option1 = db.Column(db.String())
    option2 = db.Column(db.String())
    option3 = db.Column(db.String())
    option4 = db.Column(db.String())
    answer = db.Column(db.Integer, nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False) 

class User_Subject(db.Model): 
    id = db.Column(db.Integer, primary_key=True)  
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  

class Question_Quiz(db.Model): 
    id = db.Column(db.Integer, primary_key=True)  
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False) 
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False) 


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

api.add_resource(Hello, '/hello')
api.add_resource(LoginResource, '/login')
api.add_resource(Signup, '/signup')
api.add_resource(AdminLoginResource, "/adminlogin")

if __name__ == '__main__':
    app.run(debug=True)