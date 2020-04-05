from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from quiz.models import Quiz, Question, Category
from quiz.serializers import QuizSerializer, QuestionSerializer, ImageSerializer, CategorySerializer
from quiz.permissions import IsQuizCreatorOrReadOnly


class QuizListView(APIView):
    """
    List of published quizzes.
    """
    permission_classes = (IsAuthenticatedOrReadOnly, )

    def get(self, request, format=None):
        quizzes = Quiz.objects.published()
        category = request.query_params.get('category')
        if category:
            quizzes = quizzes.filter(category__name=category)

        serializer = QuizSerializer(quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = QuizSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuizDraftsView(APIView):
    """
    List of unpublished quizzes for specific user.
    """
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        draft_quizzes = Quiz.objects.drafts(request.user.id)
        serializer = QuizSerializer(draft_quizzes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizDetailView(APIView):
    """
    Detail view of quiz, available methods are GET, PUT, DELETE
    """
    permission_classes = (IsAuthenticated, IsQuizCreatorOrReadOnly,)

    def get_object(self, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(self.request, quiz)
        return quiz

    def get(self, request, pk, format=None):
        quiz = self.get_object(pk)
        if quiz.is_published or quiz.creator == request.user:
            serializer = QuizSerializer(quiz)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):
        quiz = self.get_object(pk)
        serializer = QuizSerializer(quiz, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        quiz = self.get_object(pk)
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizPublishView(APIView):
    """
    Resource which allows to publish specific quiz instance.
    """
    permission_classes = (IsQuizCreatorOrReadOnly,)

    def get_object(self, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(self.request, quiz)
        return quiz

    def post(self, request, pk, format=None):
        quiz = self.get_object(pk)
        quiz.publish()
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)


class QuizUnpublishView(APIView):
    """
    Resource which allows to unpublish specific quiz instance.
    """
    permission_classes = (IsQuizCreatorOrReadOnly,)

    def get_object(self, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(self.request, quiz)
        return quiz

    def post(self, request, pk, format=None):
        quiz = self.get_object(pk)
        quiz.unpublish()
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status.HTTP_200_OK)


class QuestionsListView(APIView):
    """
    List of all quiz questions. Available methods: [GET, POST].
    """
    permission_classes = (IsAuthenticated, IsQuizCreatorOrReadOnly,)

    def get_queryset(self, pk):
        quiz = self.get_object(pk)
        return Quiz.objects.questions(quiz_id=pk)

    def get_object(self, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(self.request, quiz)
        return quiz

    def get(self, request, pk, format=None):
        """Return all quiz questions."""
        questions = self.get_queryset(pk)
        serializer = QuestionSerializer(questions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk, format=None):
        """Create new question."""
        quiz = self.get_object(pk)
        serializer = QuestionSerializer(
            data=request.data, context={'request': request, 'quiz_pk': quiz.pk}, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk, format=None):
    #     """Update quiz questions."""
    #     quiz = self.get_object(pk)
    #     serializer = QuestionSerializer(quiz, data=request.data, many=True)
    #     if serializer.is_valid():
    #         quiz.questions.all().delete()
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionDetailView(APIView):
    """
    Detail view of specific question's instance.

    Available methods: [GET, PUT, DELETE].
    """
    permission_classes = (IsAuthenticated, IsQuizCreatorOrReadOnly)

    def get_object(self, quiz_pk, question_pk):
        quiz = get_object_or_404(Quiz, pk=quiz_pk)
        self.check_object_permissions(self.request, quiz)
        question = get_object_or_404(Question, pk=question_pk, quiz=quiz)
        return question

    def get(self, request, quiz_pk, question_pk):
        question = self.get_object(quiz_pk, question_pk)
        serializer = QuestionSerializer(question)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, quiz_pk, question_pk):
        question = self.get_object(quiz_pk, question_pk)
        serializer = QuestionSerializer(question, data=request.data, context={
                                        'request': request, 'quiz_pk': quiz_pk})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, quiz_pk, question_pk):
        question = self.get_object(quiz_pk, question_pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class QuizImageView(APIView):
    """
    View to conduct operations on quiz avatar's image.
    """
    permission_classes = (IsQuizCreatorOrReadOnly,)

    def get_object(self, pk):
        quiz = get_object_or_404(Quiz, pk=pk)
        self.check_object_permissions(self.request, quiz)
        return quiz

    def get(self, request, pk, format=None):
        quiz = self.get_object(pk)
        if quiz.image:
            serializer = ImageSerializer(quiz.image)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, pk, format=None):
        quiz = self.get_object(pk)
        serializer = ImageSerializer(quiz, data=request.data, context={'quiz_pk': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        quiz = self.get_object(pk)
        quiz.image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryListView(APIView):
    """
    View to conduct operation on Category model.
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, format=None):
        categories = CategorySerializer(Category.objects.all(), many=True)
        return Response(categories.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
