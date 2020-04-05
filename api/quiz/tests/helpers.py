from django.contrib.auth import get_user_model
from django.conf import settings
from quiz.models import Quiz, Question, QuestionAnswer


def create_user(username: str, email: str, password: str) -> settings.AUTH_USER_MODEL:
    return get_user_model.objects.create_user(
        username=username,
        email=email,
        password=password
    )
