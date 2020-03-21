from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from user import views


urlpatterns = [
    path('quizzes/<int:pk>/start/', views.QuizUserStartView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
