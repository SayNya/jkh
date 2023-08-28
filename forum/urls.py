from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("forum/", views.forum_view, name="forum"),
    path("forum/<int:question_id>", views.question_view, name="question"),
    path("forum/<int:question_id>/remove_question", views.remove_question, name="remove_question"),
    path("forum/<int:question_id>/answer_question", views.answer_question, name="answer_question"),
    path("forum/<int:question_id>/create_comment", views.create_comment, name="create_comment"),
    path("forum/create_question", views.create_question, name="create_question"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
]
