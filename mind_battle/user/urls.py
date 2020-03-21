from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import path
from user import views


urlpatterns = [
    path('quizzes/<int:pk>/start/', views.QuizUserStartView.as_view(), name='quiz_start'),
    path('quizzes/<int:pk>/finish/', views.QuizUserFinishView.as_view(), name='quiz_finish'),
    path('quizzes/<int:quiz_pk>/questions/<int:question_pk>/answer/',
         views.QuestionUserAnswerView.as_view(), name='quiz_answer'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
