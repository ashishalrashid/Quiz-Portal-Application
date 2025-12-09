import re
from datetime import date, datetime
from flask import request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from sqlalchemy import text

from models import db
from cache import cache_get_json, cache_set_json
from extensions import limiter


class GetUserSubjects(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
    @limiter.limit("100 per minute")
    def get(self, subject_id):
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
                "start_date": row.start_date,
                "end_date": row.end_date,
                "duration": duration
            })
        return jsonify({"quizzes": quizzes})


class SearchUserQuizzes(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
    def post(self, subject_id):
        """Search quizzes by name within a subject"""
        today = date.today()
        data = request.get_json() or {}
        pattern = data.get("pattern", "").strip()

        sql = text("""
            SELECT q.id, q.name AS quiz_name, c.name AS chapter_name,
                   q.start_date, q.end_date, q.time_duration
            FROM quiz q
            JOIN chapter c ON q.chapter_id = c.id
            WHERE q.end_date >= :today
                   AND c.subject_id = :subject_id
                   AND q.start_date <= :today
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

            quiz_data = {
                "id": row.id,
                "quiz_name": row.quiz_name,
                "chapter_name": row.chapter_name,
                "start_date": row.start_date,
                "end_date": row.end_date,
                "duration": duration
            }
            quizzes.append(quiz_data)

        if pattern:
            quizzes = [q for q in quizzes if re.search(pattern, q["quiz_name"], re.IGNORECASE)]

        return jsonify({"quizzes": quizzes}), 200


class CreateUserSubject(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
    @limiter.limit("100 per minute")
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


class GetSearchOtherSubjects(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    @limiter.limit("100 per minute")
    def post(self):
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        pattern = data.get("pattern", "").strip()

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

        if pattern:
            subjects_data = [s for s in subjects_data if re.search(pattern, s["name"], re.IGNORECASE)]

        return jsonify({"subjects": subjects_data}), 200


class userGetQuiz(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
    def get(self, quiz_id):
        query = text("""
            SELECT q.*, qi.time_duration
            FROM questions AS q
            JOIN quiz AS qi ON q.quiz_id = qi.id
            WHERE q.quiz_id = :quiz_id
        """)
        result = db.session.execute(query, {"quiz_id": quiz_id}).fetchall()
        questions = []
        duration = None
        if result:
            first = result[0]._mapping
            if first.get("time_duration"):
                try:
                    duration = int(first["time_duration"].total_seconds() // 60)
                except Exception:
                    duration = first["time_duration"]
            for row in result:
                q_dict = dict(row._mapping)
                q_dict.pop("time_duration", None)
                questions.append(q_dict)
        return jsonify({"questions": questions, "duration": duration}), 200


class SubmitScore(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
    def post(self, quiz_id):
        user_id = get_jwt_identity()
        data = request.get_json()
        score = data.get("score")
        if score is None:
            return jsonify({"msg": "Score not provided"}), 400

        quiz_sql = text("""
            SELECT start_date, end_date
            FROM quiz
            WHERE id = :quiz_id
        """)
        quiz = db.session.execute(quiz_sql, {"quiz_id": quiz_id}).fetchone()
        if not quiz:
            return jsonify({"msg": "Quiz not found"}), 404

        quiz_start = quiz.start_date
        quiz_end = quiz.end_date

        quiz_start = datetime.strptime(quiz_start, "%Y-%m-%d").date() if isinstance(quiz_start, str) else quiz_start
        quiz_end = datetime.strptime(quiz_end, "%Y-%m-%d").date() if isinstance(quiz_end, str) else quiz_end

        current_date = date.today()
        if not (quiz_start <= current_date <= quiz_end):
            return jsonify({"msg": "Score outside the quiz window"}), 403

        check_sql = text("""
            SELECT id FROM scores
            WHERE quiz_id = :quiz_id AND user_id = :user_id
        """)
        existing = db.session.execute(check_sql, {"quiz_id": quiz_id, "user_id": user_id}).fetchone()
        if existing:
            return jsonify({"msg": "Score already submitted"}), 400

        sql = text("""
            INSERT INTO scores (quiz_id, user_id, score)
            VALUES (:quiz_id, :user_id, :score)
        """)
        db.session.execute(sql, {"quiz_id": quiz_id, "user_id": user_id, "score": score})
        db.session.commit()
        return jsonify({"msg": "Success"}), 201


class UrPerformance(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
    def get(self):
        user_id = get_jwt_identity()
        sql = text("""
            SELECT s.name AS subject_name, c.name AS chapter_name, q.name AS quiz_name, sc.score
            FROM scores sc
            JOIN quiz q ON sc.quiz_id = q.id
            JOIN chapter c ON q.chapter_id = c.id
            JOIN subject s ON c.subject_id = s.id
            WHERE sc.user_id = :user_id
        """)
        result = db.session.execute(sql, {"user_id": user_id}).fetchall()
        performance = [{
            "subject_name": row.subject_name,
            "chapter_name": row.chapter_name,
            "quiz_name": row.quiz_name,
            "score": row.score
        } for row in result]
        return jsonify({"performance": performance})