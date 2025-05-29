from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.contrib import messages
from django.conf import settings
import openai
import json

from .models import Course, Module, Chapter, Quiz, Assignment, QuizAnswer
from .services import generate_ai_course


openai.api_key = settings.OPENAI_API_KEY

# Inline admin
class ChapterInline(admin.TabularInline):
    model = Chapter
    extra = 0
    show_change_link = True

class QuizInline(admin.TabularInline):
    model = Quiz
    extra = 0

class AssignmentInline(admin.TabularInline):
    model = Assignment
    extra = 0

class ModuleInline(admin.TabularInline):
    model = Module
    extra = 0
    show_change_link = True

# CourseAdmin – AI struktuuri loomine ja valideerimine
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['topic', 'user', 'created_at']
    search_fields = ['topic']
    list_filter = ['user']
    inlines = [ModuleInline]
    change_form_template = "admin/course_change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:course_id>/generate-full/', self.admin_site.admin_view(self.generate_full_structure), name='generate-full-structure'),
            path('<int:course_id>/validate-course/', self.admin_site.admin_view(self.validate_course_structure), name='validate-course'),
        ]
        return custom_urls + urls

    def generate_full_structure(self, request, course_id):
        course = Course.objects.get(id=course_id)

        for module in course.modules.all():
            for chapter in module.chapters.all():
                chapter.quizzes.all().delete()
                chapter.assignments.all().delete()
            module.chapters.all().delete()
        course.modules.all().delete()

        generate_ai_course(course)
        messages.success(request, f"✅ Kursus '{course.topic}' genereeriti edukalt AI abil.")
        return redirect(f"/admin/core/course/{course_id}/change/")

    def validate_course_structure(self, request, course_id):
        course = Course.objects.get(id=course_id)
        course_data = f"Kursus: {course.topic}\n\n"
        for module in course.modules.all():
            course_data += f"  Moodul: {module.title}\n"
            for chapter in module.chapters.all():
                course_data += f"    Peatükk: {chapter.title}\n"
                course_data += f"    Sisu: {chapter.content[:200]}...\n"
                for quiz in chapter.quizzes.all():
                    course_data += f"      Quiz: {quiz.question} → {quiz.answer}\n"
                for a in chapter.assignments.all():
                    course_data += f"      Ülesanne: {a.instruction[:100]}\n"

        prompt = f"""
Analüüsi selle kursuse struktuuri kvaliteeti:
- kas moodulid ja peatükid on hästi organiseeritud
- kas quiz'id ja ülesanded on sobivad
- anna hinnang (1-10) ja parandussoovitused

{course_data}
"""

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            content = response['choices'][0]['message']['content'].strip()
            messages.success(request, f"🧠 AI hinnang:\n{content}")
        except Exception as e:
            messages.error(request, f"❌ AI viga: {e}")

        return redirect(f"/admin/core/course/{course_id}/change/")

# ChapterAdmin – quiz + assignment AI-nupud
@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ['title', 'module']
    search_fields = ['title', 'module__title']
    list_filter = ['module']
    inlines = [QuizInline, AssignmentInline]
    change_form_template = "admin/chapter_change_form.html"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('<int:chapter_id>/generate-assignment/', self.admin_site.admin_view(self.generate_assignment), name='generate-assignment'),
            path('<int:chapter_id>/generate-quiz/', self.admin_site.admin_view(self.generate_quiz), name='generate-quiz'),
        ]
        return custom_urls + urls

    def generate_assignment(self, request, chapter_id):
        chapter = Chapter.objects.get(id=chapter_id)
        prompt = f"""
Peatüki pealkiri: {chapter.title}
Sisu: {chapter.content}

Loo 1 praktiline ülesanne või kodutöö. Tagasta ainult juhis.
"""
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        instruction = response['choices'][0]['message']['content'].strip()
        Assignment.objects.create(chapter=chapter, instruction=instruction)
        messages.success(request, "✅ AI genereeris ülesande.")
        return redirect(f'/admin/core/chapter/{chapter_id}/change/')

    def generate_quiz(self, request, chapter_id):
        chapter = Chapter.objects.get(id=chapter_id)
        prompt = f"""
Peatüki pealkiri: {chapter.title}
Sisu: {chapter.content}

Loo 3 viktoriiniküsimust ja vastust.
Tagasta JSON kujul:
[
  {{
    "question": "...",
    "answer": "..."
  }}
]
"""
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )
            data = json.loads(response['choices'][0]['message']['content'])
            for item in data:
                Quiz.objects.create(chapter=chapter, question=item["question"], answer=item["answer"])
            messages.success(request, "✅ AI genereeris 3 quiz’i.")
        except Exception as e:
            messages.error(request, f"❌ Quiz genereerimise viga: {e}")
        return redirect(f'/admin/core/chapter/{chapter_id}/change/')


# Ülejäänud adminid
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'course']
    search_fields = ['title']
    list_filter = ['course']
    inlines = [ChapterInline]

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['question', 'chapter']
    search_fields = ['question']

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ['instruction', 'chapter']
    search_fields = ['instruction']

@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ['quiz', 'user', 'ai_score', 'created_at']
    search_fields = ['quiz__question', 'user__username']
    list_filter = ['user']
