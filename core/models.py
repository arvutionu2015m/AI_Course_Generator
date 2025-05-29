from django.db import models
from django.contrib.auth.models import User

class Course(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.topic} ({self.user.username})"

class Module(models.Model):
    course = models.ForeignKey(Course, related_name='modules', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.title} – {self.course.topic}"

class Chapter(models.Model):
    module = models.ForeignKey(Module, related_name='chapters', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return f"{self.module.title} → {self.title}"

class Quiz(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='quizzes', on_delete=models.CASCADE)
    question = models.CharField(max_length=500)
    answer = models.TextField()

    def __str__(self):
        return f"Quiz: {self.question[:40]}..."

class Assignment(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='assignments', on_delete=models.CASCADE)
    instruction = models.TextField()

    def __str__(self):
        return f"Ülesanne: {self.instruction[:40]}..."

class QuizAnswer(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_answer = models.TextField()
    ai_feedback = models.TextField(blank=True, null=True)
    ai_score = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('quiz', 'user')

    def __str__(self):
        return f"Vastus – {self.user.username} / {self.quiz.chapter.module.course.topic}"
