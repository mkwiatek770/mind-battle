from rest_framework import viewsets
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from quiz.models import Quiz, Question
from quiz.serializers import QuizSerializer, QuestionSerializer


class QuizView(viewsets.ModelViewSet):

    serializer_class = QuizSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        published_quizzes = Quiz.objects.published()
        # Filter by category.
        category = self.request.query_params.get('category')
        if category:
            return published_quizzes.filter(
                category__name=category)
        return published_quizzes

    @action(methods=['get'], detail=False, permission_classes=[IsAuthenticated])
    def drafts(self, request):
        """View to return list of draft quizzes for logged in user."""
        draft_quizzes = Quiz.objects.drafts(request.user.id)
        serialized_data = QuizSerializer(draft_quizzes, many=True)
        return Response(serialized_data.data, status=status.HTTP_200_OK)


class QuestionView(viewsets.ModelViewSet):

    serializer_class = QuestionSerializer

    def get_queryset(self):
        quiz_id = self.kwargs.get('parent_lookup_quiz')
        return Quiz.objects.questions(quiz_id)
