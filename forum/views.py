from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from forum.forms import QuestionForm, CommentForm
from forum.models import Question, Comment


def index(request):
    return render(request, 'forum/index.html')


def forum_view(request):
    if query := request.GET.get('q'):
        questions = Question.objects.filter(Q(title__icontains=query) | Q(text__icontains=query))
    else:
        questions = Question.objects.all()

    context = {
        'questions': questions,
        'query': query
    }
    return render(request, 'forum/forum.html', context=context)


def question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    comments = Comment.objects.filter(question=question)
    context = {
        'question': question,
        'comments': comments
    }
    return render(request, 'forum/question_page.html', context=context)


def create_question(request):
    if request.method == "POST":
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect("question", question_id=obj.id)


def remove_question(request, question_id):
    Question.objects.filter(id=question_id).delete()
    return redirect("forum")


def answer_question(request, question_id):
    qst = Question.objects.get(id=question_id)
    qst.is_closed = True
    qst.save()
    return redirect("question", question_id=qst.id)


def create_comment(request, question_id):
    if request.method == "POST":
        question = Question.objects.get(id=question_id)
        temp_dict = request.POST.copy()
        temp_dict["user"] = request.user
        temp_dict["question"] = question
        request.POST = temp_dict
        form = CommentForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("question", question_id=question.id)


def login_request(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="forum/auth/login.html", context={"login_form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")
