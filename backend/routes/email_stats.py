from flask import request, jsonify
from flask_restful import Resource
from flask_jwt_extended import jwt_required
from flask_cors import cross_origin
from extensions import limiter
from tasks.subject_stats import send_subjects_stats_email 
from celery_app import celery
from celery.result import AsyncResult

class EmailSubjectStats(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("20 per minute")
    def post(self):
        data = request.get_json() or {}
        email = data.get("email")
        if not email:
            return {"message": "email is required"}, 400

        task = send_subjects_stats_email.apply_async(args=[email])
        return {
            "task_id": task.id,
            "status_url": f"/tasks/{task.id}"
        }, 202


class TaskStatus(Resource):
    @jwt_required()
    def get(self, task_id):
        result = AsyncResult(task_id, app=celery)
        return jsonify({
            "id": task_id,
            "state": result.state,
            "result": result.result
        })
