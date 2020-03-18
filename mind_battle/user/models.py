from django.db import models
from django.conf import settings


class QuizUser(models.Model):
    """Model for quiz solved by user."""
    quiz = models.ForeignKey(
        'quiz.Quiz', on_delete=models.CASCADE, related_name='quiz_attempts')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='quiz_attempts')
    date_started = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(null=True, blank=True)

    good_answers = models.PositiveIntegerField(default=0)
    bad_answers = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name = "QuizUser"
        verbose_name_plural = "QuizUsers"

    def __str__(self) -> str:
        return f"{self.user.username}  --  {self.quiz}"

    def is_finished(self) -> bool:
        """Check if user finished solving quiz."""
        return True if self.date_finished else False

    def score(self) -> float:
        """Evaluate user result."""
        all_answers = self.good_answers + self.bad_answers
        return self.good_answers / all_answers


class QuestionUser(models.Model):
    """Model for question answered by user."""
    question = models.ForeignKey('quiz.Question', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    answer = models.ForeignKey(
        'quiz.QuestionAnswer', on_delete=models.SET_NULL,
        related_name='answers', null=True)

    class Meta:
        verbose_name = "QuestionUser"
        verbose_name_plural = "QuestionUsers"

    def __str__(self) -> str:
        return f"{self.user.username}  --  {self.question}"

    def is_correct(self) -> bool:
        """Check if user answer is correct.

        If user skip this question, return False.
        """
        if not self.answer:
            return False
        return self.answer.is_correct
