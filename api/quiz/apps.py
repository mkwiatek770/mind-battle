from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class QuizConfig(AppConfig):
    name = 'quiz'
    verbose_name = _('quizzes')

    def ready(self):
        import quiz.signals
