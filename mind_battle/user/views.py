from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from quiz.models import Quiz, Question
from quiz.permissions import IsQuizPublished


class QuizUserActionsMixin(APIView):

    permission_classes = (IsQuizPublished, IsAuthenticated,)

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
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class QuestionUserAnswerView(QuizUserActionsMixin):

    def put(self, request, quiz_pk, question_pk):
        quiz = self.get_object(quiz_pk)
        question = get_object_or_404(Question, pk=question_pk)

        if question.answer(request.user, request.data['answer']):
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
