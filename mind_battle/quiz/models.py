from django.db import models
from django.contrib.auth import get_user_model
from django.utils.text import slugify


class Quiz(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(
        'quiz.Category', related_name='quizzes', null=True, on_delete=models.SET_NULL)
    creator = models.ForeignKey(
        get_user_model(), related_name='quizzes', null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(auto_now=True)
    # image = models.ImageField()

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


class Question(models.Model):
    quiz = models.ForeignKey(
        'quiz.Quiz', on_delete=models.CASCADE, related_name="questions")
    question = models.TextField()
    # temporary solution
    good_answer = models.CharField(max_length=255)
    bad_answer_1 = models.CharField(max_length=255)
    bad_answer_2 = models.CharField(max_length=255)
    bad_answer_3 = models.CharField(max_length=255)
    explaination = models.TextField()

    good_answers = models.IntegerField(default=0)
    bad_answers = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self) -> str:
        return f"{self.question[:20]}..." if len(self.question) > 18 else self.question


class Category(models.Model):
    name = models.CharField(max_length=100)
    # image = models.ImageField()

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self) -> str:
        return self.name
