from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.db.models import Q, Count
from django.shortcuts import render, redirect, get_object_or_404

from forum.forms import QuestionForm, CommentForm
from forum.models import Question, Comment


def index(request):
    return render(request, 'forum/index.html')


@login_required()
def forum_view(request):
    if request.method == 'POST':
        form = QuestionForm(data=request.POST)
        if form.is_valid():
            obj = form.save()
            return redirect("question", question_id=obj.id)
        return render(request, 'forum/forum.html', {'form': form})

    questions = Question.objects.annotate(num_comments=Count('comments'))
    if query := request.GET.get('q'):
        questions = questions.filter((Q(title__icontains=query) | Q(text__icontains=query)))
    if ftr := request.GET.get('f') == 'nansw':
        questions = questions.filter(num_comments=0)

    form = QuestionForm()
    context = {
        'questions': questions,
        'form': form,
        'query': query,
        'filter': ftr
    }
    return render(request, 'forum/forum.html', context=context)


@login_required()
def question_view(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    comments = Comment.objects.filter(question=question)
    context = {
        'question': question,
        'comments': comments,
    }

    if request.method == 'POST':
        question = Question.objects.get(id=question_id)
        data = request.POST.copy()
        data["user"] = request.user
        data["question"] = question
        form = CommentForm(data=data)
        if form.is_valid():
            form.save()
        context['form'] = form

    context['form'] = CommentForm()
    return render(request, 'forum/question_page.html', context=context)


@login_required()
def remove_question(request, question_id):
    Question.objects.filter(id=question_id).delete()
    return redirect("forum")


@login_required()
def answer_question(request, question_id):
    qst = Question.objects.get(id=question_id)
    qst.is_closed = True
    qst.save()
    return redirect("question", question_id=qst.id)


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
        return render(request=request, template_name="forum/auth/login.html", context={"login_form": form})
    form = AuthenticationForm()
    return render(request=request, template_name="forum/auth/login.html", context={"login_form": form})


@login_required()
def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("index")


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, data=request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, form.user)
            messages.success(request, "Password changed.")
            return redirect("index")
        return render(request, "forum/auth/pass_change.html", {'form': form})

    form = PasswordChangeForm(request.user)
    return render(request, "forum/auth/pass_change.html", {'form': form})
