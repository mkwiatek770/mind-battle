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
    # zamienić listę na set, żeby nie było problemu z unique constraint

    faker = Faker("en_US")
    User = get_user_model()
    LEVEL = 0

    LEVELS = {
        0: {
            'N_CATEGORIES': 3,
            'N_USERS': 5,
            'N_QUIZZES': 10
        },
        1: {
            'N_CATEGORIES': 5,
            'N_USERS': 10,
            'N_QUIZZES': 20
        },
        2: {
            'N_CATEGORIES': 7,
            'N_USERS': 15,
            'N_QUIZZES': 50
        }
    }

    def add_arguments(self, parser):
        # Named (optional) argument
        parser.add_argument(
            '--level',
            type=int,
            help='Set how many records to insert. 0 option is default 2 - is max.',
        )

    def handle(self, *args, **options):

        # handle arguments
        if options['level'] and options['level'] in (0, 1, 2):
            self.LEVEL = options['level']
        n_categories = self.LEVELS[self.LEVEL]['N_CATEGORIES']
        n_users = self.LEVELS[self.LEVEL]['N_USERS']
        n_quizzes = self.LEVELS[self.LEVEL]['N_QUIZZES']

        self.stdout.write('Starting DB population...')

        t0 = time.perf_counter()
        categories = self.create_categories(n_categories)
        self.stdout.write(self.style.SUCCESS(f"Generated {n_categories} categories"))

        users = self.create_users(n_users)
        self.stdout.write(self.style.SUCCESS(f"Generated {n_users} users"))

        self.create_quizzes(n_quizzes, categories, users)
        self.stdout.write(self.style.SUCCESS(f"Generated {n_quizzes} quiz instances"))
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
