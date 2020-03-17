from rest_framework import viewsets
from quiz.models import Quiz, Question
from quiz.serializers import QuizSerializer, QuestionSerializer


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


class QuestionView(viewsets.ModelViewSet):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz_id = self.kwargs.get('parent_lookup_quiz')
        return Question.objects.filter(quiz__id=quiz_id)
