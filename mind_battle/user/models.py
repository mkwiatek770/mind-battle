from django.db import models
from django.contrib.auth import get_user_model


class QuizUser(models.Model):
    """Model for quiz solved by user."""
    quiz = models.ForeignKey(
        'quiz.Quiz', on_delete=models.CASCADE, related_name='quiz_attempts')
    user = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='quiz_attempts')
    date_started = models.DateTimeField(auto_now_add=True)
    date_finished = models.DateTimeField(null=True)

    good_answers = models.IntegerField(default=0)
    bad_answers = models.IntegerField(default=0)

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
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    answer = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
