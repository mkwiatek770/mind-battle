import time
import random
from typing import List
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from quiz.models import Quiz, Category, Question, QuestionAnswer


class Command(BaseCommand):
    """Command to populate DB with many records."""

    # przyjmować jako argument od użytkownika jedną z flag 0, 1, 2 gdzie 0 znaczy mało 1 średnio a 2 dużo
    # zamienić tworzenie na bulk_create

    N_CATEGORIES = 5
    N_USERS = 10
    N_QUIZZES = 10
    faker = Faker("en_US")
    User = get_user_model()

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting DB population...')

        t0 = time.perf_counter()
        categories = self.create_categories(self.N_CATEGORIES)
        self.stdout.write(self.style.SUCCESS(f"Generated {self.N_CATEGORIES} categories"))

        users = self.create_users(self.N_USERS)
        self.stdout.write(self.style.SUCCESS(f"Generated {self.N_USERS} users"))

        self.create_quizzes(self.N_QUIZZES, categories, users)
        self.stdout.write(self.style.SUCCESS(f"Generated {self.N_QUIZZES} quiz instances"))
        t1 = time.perf_counter()
        self.stdout.write(f"Time took: {t1-t0:.2f}s")

    def create_categories(self, n: int) -> List[Category]:
        return [Category.objects.create(name=self.faker.word()) for _ in range(n)]

    def create_users(self, n: int) -> List[settings.AUTH_USER_MODEL]:
        users = []
        for _ in range(n):
            profile = self.faker.profile()
            users.append(self.User.objects.create_user(
                username=profile['username'],
                password=self.faker.password(),
                email=profile['mail'],
                age=random.randint(15, 67)
            ))
        # return self.User.objects.bulk_create(users)
        return users

    def create_quizzes(self, n: int, categories: list, users: list) -> None:
        for _ in range(n):
            category = random.choice(categories)
            user = random.choice(users)
            quiz = Quiz.objects.create(
                name=self.faker.sentence(),
                creator=user,
                category=category
            )
            if random.random() > 0.5:
                quiz.publish()

            self.create_questions_to_quiz(quiz)

    def create_questions_to_quiz(self, quiz: Quiz) -> None:
        for _ in range(random.randint(4, 8)):
            question = Question.objects.create(
                quiz=quiz,
                question=f"{self.faker.sentence()}?",
                explaination=self.faker.sentence()
            )
            self.create_answers_to_question(question)

    def create_answers_to_question(self, question: Question) -> None:
        for i in range(random.randint(2, 4)):
            QuestionAnswer.objects.create(
                question=question,
                content=self.faker.word(),
                is_correct=True if i == 0 else False
            )
