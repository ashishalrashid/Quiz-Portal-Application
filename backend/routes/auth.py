from datetime import datetime
from flask import Flask, request, jsonify, make_response
from flask_cors import cross_origin
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_restful import Resource
from werkzeug.security import check_password_hash

from models import Admin, User, db
from extensions import limiter

class ProtectedRoute(Resource):
    @jwt_required()
    @limiter.limit("10 per minute")
    def get(self):
        return jsonify({"msg": "This is a protected route!"})


class LoginResource(Resource):
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
    @limiter.limit("100 per minute")
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
    @limiter.limit("100 per minute")
    def post(self):
        data = request.get_json()
        username = (data or {}).get('username')
        password = (data or {}).get('password')
        email = (data or {}).get('email')
        name = (data or {}).get('name')
        qualification = (data or {}).get('qualification')
        dob_str = (data or {}).get('dob')

        # Required fields guardrails to avoid NULL constraint errors
        missing = [field for field, val in {
            "username": username,
            "password": password,
            "email": email,
            "name": name,
            "qualification": qualification,
        }.items() if not val]
        if missing:
            return jsonify({"msg": f"Missing required fields: {', '.join(missing)}"}), 400

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