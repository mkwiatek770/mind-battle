""""Test endpoints for API."""
from rest_framework.test import APIClient
from django.test import TestCase
from django.utils import timezone
from quiz.models import (
    Quiz,
    Category,
    Question,
    QuestionAnswer
)
from quiz.serializers import (
    QuizSerializer,
    QuestionSerializer,
    QuestionAnswerSerializer
)


class TestQuizUnauthenticated(TestCase):
    """Test for quiz related endpoints for unathenticated user."""

    def setUp(self):
        self.client = APIClient()

    def test_get_all_published_quizzes(self):
        """Get all quizzes that was already published"""
        quiz_published = Quiz.objects.create(name="quiz 1")
        quiz_published.publish()
        quiz_not_published = Quiz.objects.create(name="quiz 2")

        response = self.client.get("/api/v1/quizzes/")
        serialized_data = QuizSerializer(
            Quiz.objects.published(), many=True).data

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_data)
        self.assertIn(QuizSerializer(quiz_published).data, response.data)
        self.assertNotIn(QuizSerializer(
            quiz_not_published).data, response.data)

    def test_get_quizes_filtered_by_category(self):
        """Receive all quizzes filtered by given category."""
        category_1 = Category.objects.create(name='python')
        category_2 = Category.objects.create(name='javascript')
        quiz_1 = Quiz.objects.create(name='quiz 1', category=category_1)
        quiz_2 = Quiz.objects.create(name='quiz 2', category=category_2)
        quiz_1.publish()
        quiz_2.publish()

        response = self.client.get(
            '/api/v1/quizzes/', {'category': 'python'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(QuizSerializer(quiz_1).data, response.data)
        self.assertNotIn(QuizSerializer(quiz_2).data, response.data)

    def test_get_quiz_detail(self):
        """Receive detail info about specific quiz."""
        quiz = Quiz.objects.create(name='name')
        quiz.publish()
        serialized_data = QuizSerializer(quiz).data

        response = self.client.get(f'/api/v1/quizzes/{quiz.id}/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_data)

    def test_get_quiz_detail_404_not_exist(self):
        """404 not found status code is returned if quiz does not exist."""
        response = self.client.get('/api/v1/quizzes/3123/')
        self.assertEqual(response.status_code, 404)

    def test_get_quiz_detail_404_not_published(self):
        """
        404 not found status code is returned if is not published yet.
        """
        quiz = Quiz.objects.create(name='quiz 1')

        response = self.client.get(f'/api/v1/quizzes/{quiz.id}/')

        self.assertFalse(quiz.is_published)
        self.assertEqual(response.status_code, 404)

    def test_get_all_quiz_questions(self):
        """Receive list of questions for specific quiz."""
        quiz = Quiz.objects.create(name='name')
        question_1 = Question.objects.create(
            quiz=quiz,
            question="What is your favourite color?",
            explaination="Some explaination")
        question_2 = Question.objects.create(
            quiz=quiz,
            question="What is your name?",
            explaination="Some explaination")

        serialized_data = QuestionSerializer(
            Question.objects.filter(quiz=quiz), many=True).data

        response = self.client.get(f'/api/v1/quizzes/{quiz.id}/questions/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, serialized_data)

    def test_question_returns_all_answers(self):
        """Check if answers to questions are returned."""
        quiz = Quiz.objects.create(name='quiz')
        quiz.publish()
        question = Question.objects.create(
            quiz=quiz,
            question="What is your favourite color?",
            explaination="Some explaination")
        answer_1 = QuestionAnswer.objects.create(
            question=question,
            content='Answer 1',
            is_correct=False
        )
        answer_2 = QuestionAnswer.objects.create(
            question=question,
            content='Answer 2',
            is_correct=True
        )

        response = self.client.get(
            f'/api/v1/quizzes/{quiz.id}/questions/{question.id}/')
        answers = response.data['answers']

        self.assertIn(QuestionAnswerSerializer(answer_1).data, answers)
        self.assertIn(QuestionAnswerSerializer(answer_2).data, answers)


class TestUserQuestion(TestCase):
    """Test actions suite by user for question."""

    def setUp(self):
        self.client = APIClient()

    def test_answer_to_question(self):
        """Submit answer to specific quiz question."""
        pass

    def test_change_answer_to_question(self):
        """Change already submitted answer."""
        pass


class TestQuizCreator(TestCase):
    """Test suite for quiz creator."""

    def setUp(self):
        self.client = APIClient()

    def test_get_draft_quizzes_for_user(self):
        """Test getting all drafted quizzes for creator."""
        pass

    def test_create_new_quiz(self):
        """Assure new quiz is created."""
        pass

    def test_update_quiz(self):
        """Assure existing quiz is updated."""
        pass

    def test_delete_quiz(self):
        """Assure specific quiz is removed."""
        pass

    def test_add_new_question_to_quiz(self):
        """Test add new question to existing quiz."""
        pass

    def test_update_question(self):
        """Test update question for quiz."""
        pass

    def test_delete_question(self):
        """Test remove question."""
        pass

    def test_publish_quiz_by_creator(self):
        """Assure quiz is published."""
        pass

    def test_publish_quiz_by_non_creator(self):
        """Assure publishing quiz by non creator is forbiden."""
        pass

    def test_unpublish_quiz_by_creator(self):
        """Assure quiz is unpublished"""
        pass

    def test_unpublish_quiz_by_non_creator(self):
        """Assure unpublishing quiz by non creator is not possible."""
        pass


class TestQuizAvatar(TestCase):
    """Test suite for avatar related actions for quiz."""

    def test_uploading_avatar(self):
        """Assert quiz avatar is uploaded."""
        pass

    def test_changing_avatar(self):
        """Assert quiz avatar is changed."""
        pass

    def test_removing_avatar(self):
        """Assert quiz avatar is removed."""
        pass
