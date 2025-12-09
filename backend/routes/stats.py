from flask import jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required
from flask_restful import Resource
from sqlalchemy import text

from models import db
from extensions import limiter


class GetCounts(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
    @limiter.limit("100 per minute")
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