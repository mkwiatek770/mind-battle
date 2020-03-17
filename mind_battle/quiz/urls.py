from django.urls import path
from quiz import views
from quiz.router import NestedDefaultRouter

router = NestedDefaultRouter()
quizzes_router = router.register(r'quizzes', views.QuizView, basename='quiz')
quizzes_router.register('questions', views.QuestionView,
                        basename='question', parents_query_lookups=['quiz'])
