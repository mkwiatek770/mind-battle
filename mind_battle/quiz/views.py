from rest_framework import viewsets
from quiz.models import Quiz
from quiz.serializers import QuizSerializer


class QuizView(viewsets.ModelViewSet):

    serializer_class = QuizSerializer
    queryset = Quiz.objects.filter(date_published__isnull=False)
