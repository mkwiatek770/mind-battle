from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from quiz.models import Quiz
from user.models import QuizUser


class QuizUserStartView(APIView):

    def get_object(self, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(self.request, quiz)
        return quiz

    def post(self, request, pk):
        quiz = self.get_object(pk)
        QuizUser.objects.create(quiz=quiz, user=request.user)  # create method .start_quiz_by_user()
        return Response(status=status.HTTP_204_NO_CONTENT)
