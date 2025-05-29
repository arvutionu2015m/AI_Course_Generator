from django.shortcuts import render, redirect
from .forms import CourseForm
from .models import Course
from django.contrib.auth.decorators import login_required
import openai
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404
from .models import Course
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Quiz, QuizAnswer
from .forms import QuizAnswerForm
from .services import get_ai_course_recommendation

@login_required
def create_suggested_course(request):
    courses = Course.objects.filter(user=request.user)
    topics = [c.topic for c in courses]

    suggestion = get_ai_course_recommendation(topics)
    if suggestion:
        course = Course.objects.create(user=request.user, topic=suggestion)
        generate_ai_course(course)
        return redirect('course_detail', course_id=course.id)
    return redirect('home')


def evaluate_answer(question, correct_answer, user_answer):
    prompt = f"""
Sa oled eksamihindaja. Küsimus oli: "{question}"

Õige vastus: "{correct_answer}"

Õpilase vastus: "{user_answer}"

Hinda vastust skaalal 0–10 ja anna lühike tagasiside eesti keeles. Vasta formaadis:
Hinne: X
Kommentaar: <tagasiside>
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )

    content = response['choices'][0]['message']['content']
    try:
        lines = content.strip().split('\n')
        score_line = next(l for l in lines if l.lower().startswith("hinne"))
        comment_line = next(l for l in lines if l.lower().startswith("kommentaar"))
        score = float(score_line.split(':')[1].strip())
        comment = comment_line.split(':', 1)[1].strip()
        return comment, score
    except Exception:
        return "AI ei suutnud hinnata vastust.", None

@login_required
def answer_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    try:
        answer = QuizAnswer.objects.get(quiz=quiz, user=request.user)
        form = QuizAnswerForm(instance=answer)
    except QuizAnswer.DoesNotExist:
        answer = None
        form = QuizAnswerForm()

    if request.method == 'POST':
        form = QuizAnswerForm(request.POST, instance=answer)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.quiz = quiz
            obj.user = request.user

            # Hindame AI-ga
            feedback, score = evaluate_answer(quiz.question, quiz.answer, obj.user_answer)
            obj.ai_feedback = feedback
            obj.ai_score = score
            obj.save()
            return redirect('answer_quiz', quiz_id=quiz.id)

    return render(request, 'answer_quiz.html', {'quiz': quiz, 'form': form, 'answer': answer})


@login_required
def regenerate_course(request, course_id):
    course = get_object_or_404(Course, id=course_id, user=request.user)

    # Kustuta vanad andmed
    for module in course.modules.all():
        for chapter in module.chapters.all():
            chapter.quizzes.all().delete()
            chapter.assignments.all().delete()
        module.chapters.all().delete()
    course.modules.all().delete()

    # Genereeri uuesti
    generate_ai_course(course)

    return HttpResponseRedirect(reverse('course_detail', args=[course.id]))


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id, user=request.user)
    modules = course.modules.prefetch_related('chapters__quizzes', 'chapters__assignments')
    return render(request, 'course_detail.html', {'course': course, 'modules': modules})


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


openai.api_key = settings.OPENAI_API_KEY



@login_required
def home(request):
    courses = Course.objects.filter(user=request.user)
    topics = [c.topic for c in courses]

    suggestion = None
    if topics:
        suggestion = get_ai_course_recommendation(topics)

    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.user = request.user
            course.save()
            generate_ai_course(course)
            return redirect('home')
    else:
        form = CourseForm()

    return render(request, 'home.html', {
        'form': form,
        'courses': courses,
        'suggestion': suggestion
    })


def generate_ai_course(course):
    prompt = f"Loo AI kursus teemal '{course.topic}' koos moodulite, peatükkide, ülesannetega."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    print(response['choices'][0]['message']['content'])  # TODO: parsida ja salvestada models
