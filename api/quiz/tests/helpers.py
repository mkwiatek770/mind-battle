from django.contrib.auth import get_user_model
from django.conf import settings
from quiz.models import Quiz, Question, QuestionAnswer, Category


def create_user(username: str, password: str, email: str) -> settings.AUTH_USER_MODEL:
    return get_user_model().objects.create(
        username=username,
        email=email,
        password=password
    )


def create_quiz(**kwargs) -> Quiz:
    return Quiz.objects.create(**kwargs)


def create_question(**kwargs) -> Question:
    return Question.objects.create(**kwargs)


def create_category(**kwargs) -> Category:
    return Category.objects.create(**kwargs)


def create_question_answer(**kwargs) -> QuestionAnswer:
    return QuestionAnswer.objects.create(**kwargs)
