""""Test endpoints for API."""
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
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
        self.user = get_user_model().objects.create(
            username='user1',
            password='password'
        )

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

        response = self.client.get('/api/v1/quizzes/', {'category': 'python'})

        self.assertEqual(response.status_code, 200)
        self.assertIn(QuizSerializer(quiz_1).data, response.data)
        self.assertNotIn(QuizSerializer(quiz_2).data, response.data)


class TestQuizAuthenticated(TestCase):
    """Test suite for authenticated user."""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create(
            username="user",
            password="password"
        )
        self.client.force_authenticate(user=self.user)

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

    def test_get_quiz_detail_403_not_published(self):
        """
        403 not found status code is returned if is not published yet.
        """
        quiz = Quiz.objects.create(name='quiz 1')

        response = self.client.get(f'/api/v1/quizzes/{quiz.id}/')

        self.assertFalse(quiz.is_published)
        self.assertEqual(response.status_code, 403)

    def test_get_all_quiz_questions(self):
        """Receive list of questions for specific quiz."""
        quiz = Quiz.objects.create(name='name', creator=self.user)
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
        """Check if answers to question are returned."""
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
        self.user_1 = get_user_model().objects.create(
            username='user1',
            password='password'
        )
        self.user_2 = get_user_model().objects.create(
            username='user2',
            password='password'
        )
        self.client.force_authenticate(user=self.user_1)

    def test_get_draft_quizzes_for_user(self):
        """Test getting all drafted quizzes for creator."""
        quiz_unpublished_user_1 = Quiz.objects.create(name='quiz1', creator=self.user_1)
        quiz_unpublished_user_2 = Quiz.objects.create(name='quiz2', creator=self.user_2)
        quiz_published_user_1 = Quiz.objects.create(name='quiz1published', creator=self.user_1)
        quiz_published_user_1.publish()

        response = self.client.get('/api/v1/quizzes/drafts/')

        self.assertEqual(response.status_code, 200)
        self.assertIn(QuizSerializer(quiz_unpublished_user_1).data, response.data)
        self.assertNotIn(QuizSerializer(quiz_unpublished_user_2).data, response.data)
        self.assertNotIn(QuizSerializer(quiz_published_user_1).data, response.data)

    def test_get_draft_quizzes_for_not_authenticated(self):
        """Test http 403 status code is returned for annonymous user."""
        Quiz.objects.create(name='quiz')

        self.client.logout()
        response = self.client.get('/api/v1/quizzes/drafts/')

        self.assertEqual(response.status_code, 403)

    def test_create_and_publish_new_quiz(self):
        """Assure new quiz is created and published."""
        category = Category.objects.create(name='python')
        payload_data = {
            'name': 'Quiz 1',
            'category_name': 'python',
            'publish': True,
        }

        response = self.client.post('/api/v1/quizzes/', data=payload_data)
        quiz = Quiz.objects.get(name='Quiz 1')

        self.assertEqual(response.status_code, 201)
        self.assertTrue(quiz.is_published)

    def test_create_without_publish_new_quiz(self):
        """Test quiz is created but not published."""
        category = Category.objects.create(name='python')
        payload_data = {
            'name': 'Quiz 1',
            'category_name': 'python',
            'publish': False,
        }

        response = self.client.post('/api/v1/quizzes/', data=payload_data)
        quiz = Quiz.objects.get(name='Quiz 1')

        self.assertEqual(response.status_code, 201)
        self.assertFalse(quiz.is_published)

    def test_create_new_quiz_for_not_authenticated(self):
        """Assure non authenticated user can't access this endpoint."""
        category = Category.objects.create(name='python')
        payload_data = {
            'name': 'Quiz 1',
            'category_name': 'python',
            'publish': False,
        }

        self.client.logout()
        response = self.client.post('/api/v1/quizzes/', data=payload_data)

        self.assertEqual(response.status_code, 403)
        self.assertFalse(Quiz.objects.filter(name='Quiz 1').exists())

    def test_update_quiz(self):
        """Assure existing quiz is updated."""
        category = Category.objects.create(name="python")
        category_2 = Category.objects.create(name="javascript")
        quiz = Quiz.objects.create(name="quiz v1", category=category, creator=self.user_1)

        payload_data = {
            'name': 'quiz v2',
            'category_name': 'javascript'
        }

        response = self.client.put(f"/api/v1/quizzes/{quiz.id}/", data=payload_data)
        updated_quiz = Quiz.objects.get(id=quiz.id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_quiz.name, "quiz v2")
        self.assertEqual(updated_quiz.category.name, "javascript")

    def test_update_quiz_by_non_creator(self):
        """Test non creat can't update someone else's quiz."""
        category = Category.objects.create(name='python')
        quiz = Quiz.objects.create(name="quiz v1", creator=self.user_2)

        payload_data = {
            'name': 'quiz v2',
            'category_name': 'python'
        }

        response = self.client.put(f"/api/v1/quizzes/{quiz.id}/", data=payload_data)
        quiz_obj = Quiz.objects.get(pk=quiz.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(quiz_obj.name, "quiz v1")

    def test_update_quiz_by_non_authenticated(self):
        """Test not logged in user can't update quiz."""
        quiz = Quiz.objects.create(name="quiz v1", creator=self.user_2)

        payload_data = {
            'name': 'quiz v2',
            'category_name': 'python'
        }

        self.client.logout()
        response = self.client.put(f"/api/v1/quizzes/{quiz.id}/", data=payload_data)
        quiz_obj = Quiz.objects.get(pk=quiz.id)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(quiz_obj.name, "quiz v1")

    def test_delete_quiz(self):
        """Assure specific quiz is removed."""
        quiz = Quiz.objects.create(name="quiz 1", creator=self.user_1)

        response = self.client.delete(f"/api/v1/quizzes/{quiz.id}/")

        self.assertEqual(response.status_code, 204)
        self.assertEqual(Quiz.objects.count(), 0)

    def test_delete_quiz_by_non_authenticated(self):
        """Assure non authenticated user can't delete quiz."""
        quiz = Quiz.objects.create(name="quiz 1", creator=self.user_1)

        self.client.logout()
        response = self.client.delete(f"/api/v1/quizzes/{quiz.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Quiz.objects.count(), 1)

    def test_delete_quiz_by_non_creator(self):
        """Assure non creator can't remove quiz from db."""
        quiz = Quiz.objects.create(name="quiz 1", creator=self.user_2)

        response = self.client.delete(f"/api/v1/quizzes/{quiz.id}/")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Quiz.objects.count(), 1)

    def test_add_new_question_to_quiz(self):
        """Test add new question to existing quiz."""
        quiz = Quiz.objects.create(name="quiz 1", creator=self.user_1)

        payload_data = {
            'question': 'What is your name?',
            'explaination': 'Lorem ipsum ...'
        }
        response = self.client.post(f"/api/v1/quizzes/{quiz.id}/questions/", data=payload_data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Question.objects.get(question='What is your name?').quiz, quiz)

    def test_update_question(self):
        """Test update question for quiz."""
        pass

    def test_delete_question(self):
        """Test remove question."""
        pass

    def test_publish_quiz_by_creator(self):
        """Assure quiz is published."""
        quiz = Quiz.objects.create(name="Quiz 1", creator=self.user_1)

        response = self.client.post(f"/api/v1/quizzes/{quiz.id}/publish/")

        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.data['date_published'])

    def test_publish_quiz_by_non_creator(self):
        """Assure publishing quiz by non creator is forbiden."""
        quiz = Quiz.objects.create(name="Quiz 2", creator=self.user_2)

        response = self.client.post(f"/api/v1/quizzes/{quiz.id}/publish/")
        quiz_obj = Quiz.objects.get(pk=quiz.id)

        self.assertEqual(response.status_code, 403)
        self.assertIsNone(quiz_obj.date_published)

    def test_unpublish_quiz_by_creator(self):
        """Assure quiz is unpublished"""
        quiz = Quiz.objects.create(name="Quiz 1", creator=self.user_1)
        quiz.publish()

        response = self.client.post(f"/api/v1/quizzes/{quiz.id}/unpublish/")

        self.assertEqual(response.status_code, 200)
        self.assertIsNone(response.data['date_published'])

    def test_unpublish_quiz_by_non_creator(self):
        """Assure unpublishing quiz by non creator is not possible."""
        quiz = Quiz.objects.create(name="Quiz 2", creator=self.user_2)
        quiz.publish()

        response = self.client.post(f"/api/v1/quizzes/{quiz.id}/unpublish/")
        quiz_obj = Quiz.objects.get(pk=quiz.id)

        self.assertEqual(response.status_code, 403)
        self.assertIsNotNone(quiz_obj.date_published)


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
