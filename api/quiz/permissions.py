from rest_framework.permissions import BasePermission


class IsQuizCreatorOrReadOnly(BasePermission):
    """
    Permission that check if request.user is quiz creator
    or quiz has been already published.
    """

    def has_object_permission(self, request, view, quiz):

        if quiz.creator == request.user:
            return True

        if request.method == 'GET' and quiz.date_published:
            return True


class IsQuizPublished(BasePermission):
    """Check if quiz object has been published."""

    def has_object_permission(self, request, view, quiz):
        return quiz.is_published
