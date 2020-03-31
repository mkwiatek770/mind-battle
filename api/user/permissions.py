from rest_framework.permissions import BasePermission
from quiz.models import Quiz
from user.models import UserQuiz


class IsQuizActiveForUser(BasePermission):

    def has_object_permission(self, request, view, quiz):

        user_quiz = UserQuiz.objects.filter(quiz=quiz, user=request.user)
        return user_quiz and user_quiz.first().date_finished is None
