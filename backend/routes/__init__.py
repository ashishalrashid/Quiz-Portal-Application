from flask_restful import Api
from .auth import LoginResource, AdminLoginResource, Signup, ProtectedRoute
from .admin import (
    CreateSubject, EditSubject, DeleteSubject, GetSubject, GetSearchSubject,
    GetUsers, GetSearchUser, EditUser, DeleteUser,
    GetChapter, CreateChapter, EditChapter, DeleteChapter,
    CreateQuiz, GetQuiz, GetSearchQuiz, EditQuiz, DeleteQuiz,
    CreateQuestion, GetQuestions, GetSearchQuestions, EditQuestion, DeleteQuestion
)
from .user import (
    GetUserSubjects, GetUserQuizzes, SearchUserQuizzes,
    CreateUserSubject, GetOtherSubjects, GetSearchOtherSubjects,
    userGetQuiz, SubmitScore, UrPerformance
)
from .stats import GetCounts, SubjectStats

from .email_stats import EmailSubjectStats, TaskStatus

def register_resources(api):
    """Register all API resources"""
    api.add_resource(ProtectedRoute, "/protected")
    
    # Auth routes
    api.add_resource(LoginResource, "/login")
    api.add_resource(Signup, "/signup")
    api.add_resource(AdminLoginResource, "/adminlogin")
    
    # Subject routes
    api.add_resource(CreateSubject, "/createsubject")
    api.add_resource(EditSubject, "/editsubject/<int:subject_id>")
    api.add_resource(DeleteSubject, "/deletesubject/<int:subject_id>")
    api.add_resource(GetSubject, "/getsubjects")
    api.add_resource(GetSearchSubject, "/getsearchsubject")
    
    # User management routes
    api.add_resource(GetUsers, "/getusers")
    api.add_resource(GetSearchUser, "/getsearchuser")
    api.add_resource(EditUser, "/edituser/<int:user_id>")
    api.add_resource(DeleteUser, "/deleteuser/<int:user_id>")
    
    # Chapter routes
    api.add_resource(GetChapter, "/getchapter/<int:subject_id>")
    api.add_resource(CreateChapter, "/createchapter/<int:subject_id>")
    api.add_resource(EditChapter, "/editchapter/<int:chapter_id>")
    api.add_resource(DeleteChapter, "/deletechapter/<int:chapter_id>")
    
    # Quiz routes
    api.add_resource(CreateQuiz, "/createquiz/<int:chapter_id>")
    api.add_resource(GetQuiz, "/getquiz/<int:chapter_id>")
    api.add_resource(GetSearchQuiz, "/getsearchquiz/<int:chapter_id>")
    api.add_resource(EditQuiz, "/editquiz/<int:quiz_id>")
    api.add_resource(DeleteQuiz, "/deletequiz/<int:quiz_id>")
    
    # Question routes
    api.add_resource(CreateQuestion, "/createquestion/<int:quiz_id>")
    api.add_resource(GetQuestions, "/getquestion/<int:quiz_id>")
    api.add_resource(GetSearchQuestions, "/getsearchquestions/<int:quiz_id>")
    api.add_resource(EditQuestion, "/editquestion/<int:question_id>")
    api.add_resource(DeleteQuestion, "/deletequestion/<int:question_id>")
    
    # User subject routes
    api.add_resource(GetUserSubjects, "/getus")
    api.add_resource(GetUserQuizzes, "/getuserquizzes/<int:subject_id>")
    api.add_resource(SearchUserQuizzes, "/searchuserquizzes/<int:subject_id>")
    api.add_resource(CreateUserSubject, "/createusersubject/<int:subject_id>")
    api.add_resource(GetOtherSubjects, "/getothersubjects")
    api.add_resource(GetSearchOtherSubjects, "/getsearchothersubjects")
    
    # Quiz taking routes
    api.add_resource(userGetQuiz, "/usergetquiz/<int:quiz_id>")
    api.add_resource(SubmitScore, "/submitscore/<int:quiz_id>")
    api.add_resource(UrPerformance, "/yourperformance")
    
    # Stats routes
    api.add_resource(GetCounts, "/getcounts")
    api.add_resource(SubjectStats, "/subjectstats")

    # Email stats
    api.add_resource(EmailSubjectStats, "/email-subject-stats")
    api.add_resource(TaskStatus, "/tasks/<string:task_id>")