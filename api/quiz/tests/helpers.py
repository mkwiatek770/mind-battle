from django.contrib.auth import get_user_model
from django.conf import settings
from quiz.models import Quiz, Question, QuestionAnswer


def create_user(username: str, password: str, email: str) -> settings.AUTH_USER_MODEL:
    return get_user_model().objects.create(
        username=username,
        email=email,
        password=password
    )


def create_quiz(**kwargs):
    return Quiz.objects.create(**kwargs)
