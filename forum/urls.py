from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("forum", views.forum_view, name="forum"),
    path("forum/<int:question_id>", views.question_view, name="question"),
    path("forum/<int:question_id>/remove_question", views.remove_question, name="remove_question"),
    path("forum/<int:question_id>/answer_question", views.answer_question, name="answer_question"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("reset_password/", views.change_password, name="reset_password"),
]
