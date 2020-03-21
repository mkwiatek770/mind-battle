from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from quiz.models import Quiz
from quiz.permissions import IsQuizPublished
from user.models import QuizUser


class QuizUserActionsMixin(APIView):

    permission_classes = (IsQuizPublished,)

    def get_object(self, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(self.request, quiz)
        return quiz


class QuizUserStartView(QuizUserActionsMixin):

    def post(self, request, pk):
        quiz = self.get_object(pk)
        quiz.start_quiz(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizUserFinishView(QuizUserActionsMixin):

    def post(self, request, pk):
        quiz = self.get_object(pk)
        if quiz.finish_quiz(request.user):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
