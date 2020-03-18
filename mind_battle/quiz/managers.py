from django.db import models


class QuizQueryset(models.QuerySet):
    """Custom quiz queryset class."""

    def published(self):
        """Return queryset of published quizzes."""
        return self.filter(date_published__isnull=False).order_by('-date_published')

    def draft(self):
        """Return unpublished quizzes."""
        return self.filter(date_published__isnull=True).order_by('-date_modified')

    def questions(self, quiz_id):
        """Return all quiz questions."""
        return self.get(pk=quiz_id).questions.all()


class QuizManager(models.Manager):
    """Custom quiz manager."""

    def get_queryset(self):
        return QuizQueryset(model=self.model, using=self._db)

    def get_published(self):
        """Return queryset of published quizzes."""
        return self.get_queryset().published()

    def get_drafts(self):
        """Return unpublished quizzes."""
        return self.get_queryset().draft()

    def get_questions(self, quiz_id):
        """Return all quiz questions."""
        return self.get_queryset().questions(quiz_id)
