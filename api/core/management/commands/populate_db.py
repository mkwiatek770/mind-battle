import time
import random
from typing import List
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from django.utils import timezone
from quiz.models import Quiz, Category, Question, QuestionAnswer


class Command(BaseCommand):
    """Command to populate DB with many records."""

    faker = Faker("en_US")
    User = get_user_model()
    LEVEL = 0
    LEVELS = {
        'N_CATEGORIES': [3, 5, 10],
        'N_USERS': [5, 10, 30],
        'N_QUIZZES': [7, 15, 50]
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
        n_categories = self.LEVELS['N_CATEGORIES'][self.LEVEL]
        n_users = self.LEVELS['N_USERS'][self.LEVEL]
        n_quizzes = self.LEVELS['N_QUIZZES'][self.LEVEL]

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
        return [Category.objects.create(name=f"{self.faker.word()}{random.randint(1, 1000)}") for i in range(n)]

    def create_users(self, n: int) -> List[settings.AUTH_USER_MODEL]:
        users = []
        date_before = timezone.now()

        for _ in range(n):
            profile = self.faker.profile()
            users.append(self.User(
                username=profile['username'],
                password=self.faker.password(),  # passwords are not hashed!!
                email=profile['mail'],
                age=random.randint(15, 67)
            ))
        self.User.objects.bulk_create(users)
        return self.User.objects.filter(date_joined__gt=date_before)

    def create_quizzes(self, n: int, categories: list, users: list) -> None:
        quizzes = []
        date_before = timezone.now()

        for i in range(n):
            category = random.choice(categories)
            user = random.choice(users)
            quizzes.append(Quiz(
                name=f"{self.faker.sentence()}{i}",
                creator=user,
                category=category,
                date_published=timezone.now() if random.random() > 0.5 else None
            ))
        Quiz.objects.bulk_create(quizzes)
        for quiz in Quiz.objects.filter(date_created__gt=date_before):
            self.create_questions_to_quiz(quiz)

    def create_questions_to_quiz(self, quiz: Quiz) -> None:
        how_many = random.randint(4, 8)
        question_objs = []
        questions = {f"{self.faker.sentence()}{i}?" for i in range(how_many)}
        for question in questions:
            question_objs.append(Question(
                quiz=quiz,
                question=question,
                explaination=self.faker.sentence()
            ))
        Question.objects.bulk_create(question_objs)

        for question in Question.objects.filter(question__in=questions):
            self.create_answers_to_question(question)

    def create_answers_to_question(self, question: Question) -> None:
        answers = []
        for i in range(random.randint(2, 4)):
            answers.append(QuestionAnswer(
                question=question,
                content=self.faker.word(),
                is_correct=True if i == 0 else False
            ))
        QuestionAnswer.objects.bulk_create(answers, ignore_conflicts=True)
