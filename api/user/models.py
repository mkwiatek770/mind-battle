from django.db import models
from django.db.models import Q
from django.conf import settings
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    # make email field required
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=30, unique=True)
    age = models.PositiveIntegerField(default=18)

    # USERNAME_FIELD = ['username', 'email']

    @property
    def is_adult(self) -> bool:
        """Check if user is greater or equal 18 years old."""
        return self.age >= 18

    class Meta:
        constraints = [
            models.CheckConstraint(check=~models.Q(username=""), name="non_empty_username"),
        ]


class UserQuiz(models.Model):
    """Model for quiz solved by user."""
    quiz = models.ForeignKey(
        'quiz.Quiz', on_delete=models.CASCADE, related_name='attempts')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='users')
    date_started = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(null=True, blank=True)

    good_answers = models.PositiveIntegerField(default=0)
    bad_answers = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "UserQuiz"
        verbose_name_plural = "UserQuizs"

    def __str__(self) -> str:
        return f"{self.user.username}  --  {self.quiz}"

    def is_finished(self) -> bool:
        """Check if user finished solving quiz."""
        return True if self.date_finished else False

    def score(self) -> float:
        """Evaluate user result."""
        all_answers = self.good_answers + self.bad_answers
        try:
            return self.good_answers / all_answers
        except ZeroDivisionError:
            return 0


class UserAnswer(models.Model):
    """Model for question answered by user."""
    question = models.ForeignKey('quiz.Question', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    answer = models.ForeignKey(
        'quiz.QuestionAnswer', on_delete=models.SET_NULL,
        related_name='answers', null=True)

    class Meta:
        verbose_name = "UserAnswer"
        verbose_name_plural = "UserAnswers"

    def __str__(self) -> str:
        return f"{self.user.username}  --  {self.question}"

    def is_correct(self) -> bool:
        """Check if user answer is correct.

        If user skip this question, return False.
        """
        if not self.answer:
            return False
        return self.answer.is_correct
