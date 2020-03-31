import os
from django.db import models
from django.db.models import Sum, Count, Case, When, Value
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.utils import timezone
from quiz.managers import QuizManager
from mind_battle.helpers import get_quiz_image_location
from user.models import QuizUser, UserAnswer

DEFAULT_IMG_URL = 'https://cdn.pixabay.com/photo/2015/02/24/15/41/dog-647528_960_720.jpg'


class Quiz(models.Model):

    name = models.CharField(max_length=200, unique=True)
    category = models.ForeignKey(
        'quiz.Category', related_name='quizzes', null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='quizzes', null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(null=True, blank=True)
    date_modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True, upload_to=get_quiz_image_location,
                              default='default_quiz.jpeg')

    # overwrite default manager
    objects = QuizManager()

    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def __str__(self) -> str:
        return self.name

    @property
    def is_published(self) -> bool:
        """Flag property to tell if quiz was published."""
        return True if self.date_published else False

    @property
    def slug(self) -> str:
        """Return slugified version of quiz name."""
        return slugify(self.name)

    def publish(self) -> None:
        """Publish quiz if it hasn't been already published."""
        if not self.is_published:
            self.date_published = timezone.now()
            self.save()

    def unpublish(self) -> None:
        """Unpublish quiz."""
        self.date_published = None
        self.save()

    def start_quiz(self, user) -> None:
        """Start quiz by user."""
        obj = QuizUser.objects.filter(user=user, quiz=self).first()
        if obj:
            obj.delete()
        QuizUser.objects.create(user=user, quiz=self)

    def finish_quiz(self, user) -> bool:
        """Finish quiz by user. Quiz must be started to finish it."""
        obj = QuizUser.objects.filter(user=user, quiz=self).first()
        if obj:
            obj.date_finished = timezone.now()
            obj.save()
            return True
        return False

    def get_absolute_url(self):
        return reverse("quiz_detail", kwargs={"pk": self.pk})


class Question(models.Model):
    quiz = models.ForeignKey(
        'quiz.Quiz', on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    explanation = models.TextField()

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        return f"{self.question[:20]}..." if len(self.question) > 18 else self.question

    @property
    def good_answers(self) -> int:
        result = self.answers.all().aggregate(total=Sum('is_correct'))
        return result['total']

    @property
    def bad_answers(self) -> int:
        # maybe there is easier way ...
        result = self.answers.all().aggregate(
            total=Count(
                Case(When(is_correct=False, then=Value(1)))
            )
        )
        return result['total']

    def answer(self, user, answer_pk) -> bool:
        """Answer to quiz's question by specific user."""
        answer_obj = QuestionAnswer.objects.get(id=answer_pk)
        question_obj = UserAnswer.objects.filter(user=user, question=self).first()

        quiz_user_obj = QuizUser.objects.filter(user=user, quiz=self.quiz).first()
        if quiz_user_obj:
            if quiz_user_obj.date_finished:
                return False
        else:
            return False

        if question_obj:
            question_obj.answer = answer_obj
            question_obj.save()
        else:
            UserAnswer.objects.create(
                user=user,
                question=self,
                answer=answer_obj
            )
        return True

    def get_absolute_url(self):
        return reverse("question_detail", kwargs={"quiz_pk": self.quiz.pk, "question_pk": self.pk})


class QuestionAnswer(models.Model):
    question = models.ForeignKey(
        'quiz.Question', on_delete=models.CASCADE, related_name='answers')
    content = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    # counter = models.PositiveIntegerField(default=0

    class Meta:
        verbose_name = "QuestionAnswer"
        verbose_name_plural = "QuestionAnswers"

    def __str__(self) -> str:
        return f"Answer: {self.content} for question: {self.question}"


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    image = models.ImageField(null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name
