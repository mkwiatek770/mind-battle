from rest_framework import viewsets
from quiz.models import Quiz
from quiz.serializers import QuizSerializer


class QuizView(viewsets.ModelViewSet):

    serializer_class = QuizSerializer

    def get_queryset(self):
        published_quizzes = Quiz.objects.filter(date_published__isnull=False)
        # category filtering
        category = self.request.query_params.get('category')
        if category:
            return published_quizzes.filter(
                category__name=category)
        return published_quizzes
