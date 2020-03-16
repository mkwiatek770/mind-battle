from django.db import models
from django.contrib.auth import get_user_model


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

    @property
    def is_published(self) -> bool:
        """Flag property to tell if quiz was published."""
        return True if self.date_published else False


class Category(models.Model):
    name = models.CharField(max_length=100)
    # image = models.ImageField()
