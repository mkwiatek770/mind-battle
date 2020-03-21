from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from user import views


urlpatterns = [
    path('quizzes/<int:pk>/start/', views.QuizUserStartView.as_view()),
    path('quizzes/<int:pk>/finish/', views.QuizUserFinishView.as_view()),
    path('quizzes/<int:quiz_pk>/questions/<int:question_pk>/answer/',
         views.QuestionUserAnswerView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
