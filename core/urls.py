from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('suggested/create/', views.create_suggested_course, name='create_suggested_course'),
    path('quiz/<int:quiz_id>/answer/', views.answer_quiz, name='answer_quiz'),
    path('course/<int:course_id>/regenerate/', views.regenerate_course, name='regenerate_course'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),
]
