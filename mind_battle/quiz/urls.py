from rest_framework import routers
from quiz import views

router = routers.DefaultRouter()
router.register(r'quizzes', views.QuizView, basename='quiz')
