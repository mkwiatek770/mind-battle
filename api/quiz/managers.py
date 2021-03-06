from django.db import models


class QuizQueryset(models.QuerySet):
    """Custom quiz queryset class."""

    def get_published(self):
        """Return queryset of published quizzes."""
        return self.filter(date_published__isnull=False).order_by('-date_published')

    def get_drafts(self, user_id: int):
        """Return unpublished quizzes."""
        return self.filter(date_published__isnull=True, creator__id=user_id).order_by('-date_modified')

    def get_questions(self, quiz_id: int):
        """Return all quiz questions."""
        return self.get(pk=quiz_id).questions.all().prefetch_related('answers')


class QuizManager(models.Manager):
    """Custom quiz manager."""

    def get_queryset(self):
        return QuizQueryset(model=self.model, using=self._db)

    def published(self):
        """Return queryset of published quizzes."""
        return self.get_queryset().get_published()

    def drafts(self, user_id: int):
        """Return unpublished quizzes for specific user."""
        return self.get_queryset().get_drafts(user_id)

    def questions(self, quiz_id: int):
        """Return all quiz questions."""
        return self.get_queryset().get_questions(quiz_id)
