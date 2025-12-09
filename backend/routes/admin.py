import re
from datetime import datetime
from flask import request, jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_restful import Resource
from sqlalchemy import text

from models import Subject, User, Chapter, Quiz, Questions, db
from cache import cache_delete_pattern, cache_get_json, cache_set_json

limiter = Limiter(get_remote_address, default_limits=["2000 per day", "500 per hour"])


# ============ SUBJECT CRUD ============

class CreateSubject(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    @limiter.limit("100 per minute")
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
        cache_delete_pattern("subjects:*")
        return jsonify({
            "msg": "Subject created successfully",
            "subject": {"id": subject.id, "name": subject.name, "description": subject.description}
        }), 201


class EditSubject(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    @limiter.limit("100 per minute")
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
        cache_delete_pattern("subjects:*")
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
    @limiter.limit("100 per minute")
    def delete(self, subject_id):
        if get_jwt_identity() != "admin":
            return jsonify({"msg": "Only admin can delete subjects"}), 403
        subject = Subject.query.get(subject_id)
        if not subject:
            return jsonify({"msg": "Subject not found"}), 404
        db.session.delete(subject)
        db.session.commit()
        cache_delete_pattern("subjects:*")
        return jsonify({"msg": "Subject and related entries deleted successfully"}), 200


class GetSubject(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    @limiter.limit("100 per minute")
    def get(self):
        cache_key = "subjects:all"
        cached = cache_get_json(cache_key)
        if cached is not None:
            return jsonify(cached), 200

        subjects = Subject.query.all()
        subjects_data = [
            {"id": subject.id, "name": subject.name, "description": subject.description}
            for subject in subjects
        ]
        response = {"subjects": subjects_data}
        cache_set_json(cache_key, response, ex=60)
        return jsonify(response), 200


class GetSearchSubject(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def post(self):
        data = request.get_json() or {}
        pattern = data.get("pattern", "")
        subjects = Subject.query.all()
        if pattern:
            matched = [subject for subject in subjects if re.search(pattern, subject.name, re.IGNORECASE)]
        else:
            matched = subjects
        subjects_data = [{"id": subject.id, "name": subject.name, "description": subject.description} for subject in matched]
        return jsonify({"subjects": subjects_data}), 200


# ============ USER CRUD ============

class GetUsers(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    @limiter.limit("100 per minute")
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


class GetSearchUser(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def post(self):
        data = request.get_json() or {}
        pattern = data.get("pattern", "")
        users = User.query.all()
        if pattern:
            matched = [user for user in users if re.search(pattern, user.username, re.IGNORECASE)]
        else:
            matched = users
        users_data = [{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "qualification": user.qualification,
            "dob": user.dob.strftime("%Y-%m-%d") if user.dob else None
        } for user in matched]
        return jsonify({"users": users_data}), 200


class EditUser(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    @limiter.limit("100 per minute")
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
    @limiter.limit("100 per minute")
    def delete(self, user_id):
        if get_jwt_identity() != "admin":
            return jsonify({"msg": "Only admin can delete users"}), 403

        sql = text("DELETE FROM user WHERE id = :user_id")
        result = db.session.execute(sql, {"user_id": user_id})

        if result.rowcount == 0:
            return jsonify({"msg": "User not found"}), 404

        db.session.commit()
        return jsonify({"msg": "User deleted successfully"}), 200


# ============ CHAPTER CRUD ============

class GetChapter(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
    @limiter.limit("100 per minute")
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
    @limiter.limit("100 per minute")
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
    @limiter.limit("100 per minute")
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


# ============ QUIZ CRUD ============

class CreateQuiz(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
        cache_delete_pattern("quizzes:*")
        return {"msg": "Quiz created successfully"}, 201


class GetQuiz(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
    def get(self, chapter_id):
        cache_key = f"quizzes:{chapter_id}"
        cached = cache_get_json(cache_key)
        if cached is not None:
            return jsonify(cached), 200
        try:
            query = text("""
                SELECT id, name, chapter_id, start_date, end_date, time_duration
                FROM quiz
                WHERE chapter_id = :chapter_id
            """)
            result = db.session.execute(query, {"chapter_id": chapter_id}).fetchall()

            if not result:
                return jsonify({"quizzes": []}), 200

            quizzes_list = []
            base = datetime(1970, 1, 1)

            for row in result:
                q_dict = dict(row._mapping)

                if isinstance(q_dict["time_duration"], str):
                    try:
                        dt = datetime.strptime(q_dict["time_duration"], "%Y-%m-%d %H:%M:%S.%f")
                        q_dict["time_duration"] = int((dt - base).total_seconds() // 60)
                    except ValueError:
                        q_dict["time_duration"] = None
                elif hasattr(q_dict["time_duration"], "total_seconds"):
                    q_dict["time_duration"] = int(q_dict["time_duration"].total_seconds() // 60)
                else:
                    q_dict["time_duration"] = int(q_dict["time_duration"]) if q_dict["time_duration"] else None

                quizzes_list.append(q_dict)

            response = {"quizzes": quizzes_list}
            cache_set_json(cache_key, response, ex=60)
            return jsonify(response), 200

        except Exception as e:
            print(f"Error in GetQuiz: {e}")
            return jsonify({"error": "Internal Server Error"}), 500


class GetSearchQuiz(Resource):
    @cross_origin(origins="http://localhost:5173")
    @jwt_required()
    def post(self, chapter_id):
        data = request.get_json() or {}
        pattern = data.get("pattern", "").strip()

        quizzes = db.session.execute(
            text("""
                SELECT id, name, chapter_id, start_date, end_date, time_duration
                FROM quiz
                WHERE chapter_id = :chapter_id
            """),
            {"chapter_id": chapter_id}
        ).fetchall()

        quizzes_list = [
            {
                "id": q.id,
                "name": q.name,
                "chapter_id": q.chapter_id,
                "start_date": q.start_date,
                "end_date": q.end_date,
                "time_duration": q.time_duration
            }
            for q in quizzes
        ]
        if pattern:
            quizzes_list = [q for q in quizzes_list if re.search(re.escape(pattern), q["name"], re.IGNORECASE)]

        return jsonify({"quizzes": quizzes_list}), 200


class EditQuiz(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
        cache_delete_pattern("quizzes:*")
        return {"msg": "Quiz updated successfully"}, 200


class DeleteQuiz(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
        cache_delete_pattern("quizzes:*")
        cache_delete_pattern("questions:*")
        return {"msg": "Quiz deleted successfully"}, 200


# ============ QUESTION CRUD ============

class CreateQuestion(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
        try:
            quiz_check = db.session.execute(db.text("SELECT id FROM quiz WHERE id = :quiz_id"), {"quiz_id": quiz_id}).fetchone()
            if not quiz_check:
                return {"msg": "Quiz ID not found"}, 404

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

            db.session.flush()
            db.session.commit()
            cache_delete_pattern("questions:*")
            return {"msg": "Question created successfully"}, 201

        except Exception as e:
            db.session.rollback()
            print(f"Error creating question: {e}")
            return {"msg": "Internal Server Error", "error": str(e)}, 500


class GetQuestions(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def get(self, quiz_id):
        cache_key = f"questions:{quiz_id}"
        cached = cache_get_json(cache_key)
        if cached is not None:
            return jsonify(cached), 200

        questions = db.session.execute(
            db.text("""
                SELECT q.id, q.question, q.option1, q.option2, q.option3, q.option4, q.answer
                FROM questions q
                WHERE q.quiz_id = :quiz_id
            """),
            {"quiz_id": quiz_id}
        ).fetchall()
        response = [{
            "id": q.id,
            "question": q.question,
            "options": [q.option1, q.option2, q.option3, q.option4],
            "answer": q.answer
        } for q in questions]
        cache_set_json(cache_key, response, ex=60)
        return jsonify(response), 200


class GetSearchQuestions(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    def post(self, quiz_id):
        data = request.get_json() or {}
        pattern = data.get("pattern", "").strip()

        questions = db.session.execute(
            text("""
                SELECT id, question, option1, option2, option3, option4, answer
                FROM questions
                WHERE quiz_id = :quiz_id
            """),
            {"quiz_id": quiz_id}
        ).fetchall()

        questions_list = [
            {
                "id": q.id,
                "question": q.question,
                "options": [q.option1, q.option2, q.option3, q.option4],
                "answer": q.answer
            }
            for q in questions
        ]

        if pattern:
            questions_list = [q for q in questions_list if re.search(pattern, q["question"], re.IGNORECASE)]

        return jsonify({"questions": questions_list}), 200


class EditQuestion(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
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
        cache_delete_pattern("questions:*")
        return {"msg": "Question updated"}, 200


class DeleteQuestion(Resource):
    @jwt_required()
    @cross_origin(origins="http://localhost:5173")
    @limiter.limit("100 per minute")
    def delete(self, question_id):
        if get_jwt_identity() != "admin":
            return {"msg": "Not authorized"}, 403
        db.session.execute(
            db.text("DELETE FROM questions WHERE id = :question_id"),
            {"question_id": question_id}
        )
        db.session.commit()
        cache_delete_pattern("questions:*")
        return {"msg": "Question deleted"}, 200