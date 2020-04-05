""""Test endpoints for API."""
from io import BytesIO
from PIL import Image
from unittest import mock
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from rest_framework.test import force_authenticate

from django.utils import timezone
from django.core.files.base import File
from django.urls import reverse

from quiz.models import (
    Quiz,
    Category,
    Question,
    QuestionAnswer
)
from quiz.serializers import (
    QuizSerializer,
    QuestionSerializer,
    QuestionAnswerSerializer,
    CategorySerializer
)
from quiz.tests.helpers import (
    create_category,
    create_user,
    create_quiz,
    create_question,
    create_question_answer,
)


class TestQuizUnauthenticated(APITestCase):
    """Test for quiz related endpoints for unathenticated user."""

    def setUp(self):
        self.user = create_user("user1", "password", "email@gmail.com")
        category_1 = create_category(name='python')
        category_2 = create_category(name='javascript')
        self.quiz_published_1 = create_quiz(
            name='quiz 1', category=category_1, date_published=timezone.now())
        self.quiz_published_2 = create_quiz(
            name='quiz 2', category=category_2, date_published=timezone.now())
        self.quiz_not_published = create_quiz(name="quiz 3")

    def test_get_all_published_quizzes(self):
        """Get all quizzes that was already published"""
        response = self.client.get(reverse("quiz_list"))
        serialized_data = QuizSerializer(Quiz.objects.published(), many=True).data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_data)
        self.assertIn(QuizSerializer(self.quiz_published_1).data, response.data)
        self.assertIn(QuizSerializer(self.quiz_published_2).data, response.data)
        self.assertNotIn(QuizSerializer(self.quiz_not_published).data, response.data)

    def test_get_quizes_filtered_by_category(self):
        """Receive all quizzes filtered by given category."""
        response = self.client.get(reverse("quiz_list"), {'category': 'python'})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(QuizSerializer(self.quiz_published_1).data, response.data)
        self.assertNotIn(QuizSerializer(self.quiz_published_2).data, response.data)


class TestQuizAuthenticated(APITestCase):
    """Test suite for authenticated user."""

    def setUp(self):
        self.user = create_user("user", "password", "email@gmail.com")
        self.client.force_authenticate(user=self.user)

    def test_get_quiz_detail(self):
        """Receive detail info about specific quiz."""
        quiz = create_quiz(name='name', date_published=timezone.now())
        serialized_data = QuizSerializer(quiz).data

        response = self.client.get(reverse('quiz_detail', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_data)

    def test_get_quiz_detail_404_not_exist(self):
        """404 not found status code is returned if quiz does not exist."""
        response = self.client.get(reverse('quiz_detail', args=(31231,)))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_quiz_detail_403_not_published(self):
        """
        403 not found status code is returned if is not published yet.
        """
        quiz = create_quiz(name='quiz 1')

        response = self.client.get(reverse('quiz_detail', args=(quiz.id,)))

        self.assertFalse(quiz.is_published)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_all_quiz_questions(self):
        """Receive list of questions for specific quiz."""
        quiz = create_quiz(name='name', creator=self.user)
        question_1 = create_question(
            quiz=quiz,
            question="What is your favourite color?",
            explanation="Some explanation")
        question_2 = create_question(
            quiz=quiz,
            question="What is your name?",
            explanation="Some explanation")

        serialized_data = QuestionSerializer(
            Question.objects.filter(quiz=quiz), many=True).data

        response = self.client.get(reverse('question_list', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_data)

    def test_question_returns_all_answers(self):
        """Check if answers to question are returned."""
        quiz = create_quiz(name='quiz', date_published=timezone.now())

        question = create_question(
            quiz=quiz,
            question="What is your favourite color?",
            explanation="Some explanation")
        answer_1 = create_question_answer(
            question=question,
            content='Answer 1',
            is_correct=False
        )
        answer_2 = create_question_answer(
            question=question,
            content='Answer 2',
            is_correct=True
        )

        response = self.client.get(reverse('question_detail', args=(quiz.id, question.id)))

        answers = response.data['answers']

        self.assertIn(QuestionAnswerSerializer(answer_1).data, answers)
        self.assertIn(QuestionAnswerSerializer(answer_2).data, answers)


class TestQuizCreator(APITestCase):
    """Test suite for quiz creator."""

    def setUp(self):
        self.user_1 = create_user(username='user1', password='password', email='email@gmail.com')
        self.user_2 = create_user(username='user2', password='password', email='email2@gmail.com')
        self.client.force_authenticate(user=self.user_1)

    def test_get_draft_quizzes_for_user(self):
        """Test getting all drafted quizzes for creator."""
        quiz_unpublished_user_1 = create_quiz(name='quiz1', creator=self.user_1)
        quiz_unpublished_user_2 = create_quiz(name='quiz2', creator=self.user_2)
        quiz_published_user_1 = create_quiz(
            name='quiz1published', creator=self.user_1, date_published=timezone.now())

        response = self.client.get(reverse('quiz_drafts'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(QuizSerializer(quiz_unpublished_user_1).data, response.data)
        self.assertNotIn(QuizSerializer(quiz_unpublished_user_2).data, response.data)
        self.assertNotIn(QuizSerializer(quiz_published_user_1).data, response.data)

    def test_get_draft_quizzes_for_not_authenticated(self):
        """Test http 403 status code is returned for annonymous user."""
        create_quiz(name='quiz')

        self.client.logout()
        response = self.client.get(reverse('quiz_drafts'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_and_publish_new_quiz(self):
        """Assure new quiz is created and published."""
        category = create_category(name='python')
        payload_data = {
            'name': 'Quiz 1',
            'category_name': 'python',
            'publish': True,
        }

        response = self.client.post(reverse('quiz_list'), data=payload_data)
        quiz = Quiz.objects.get(name='Quiz 1')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(quiz.is_published)

    def test_create_without_publish_new_quiz(self):
        """Test quiz is created but not published."""
        category = create_category(name='python')
        payload_data = {
            'name': 'Quiz 1',
            'category_name': 'python',
            'publish': False,
        }

        response = self.client.post(reverse('quiz_list'), data=payload_data)
        quiz = Quiz.objects.get(name='Quiz 1')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(quiz.is_published)

    def test_create_new_quiz_for_not_authenticated(self):
        """Assure non authenticated user can't access this endpoint."""
        category = create_category(name='python')
        payload_data = {
            'name': 'Quiz 1',
            'category_name': 'python',
            'publish': False,
        }

        self.client.logout()
        response = self.client.post(reverse('quiz_list'), data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Quiz.objects.filter(name='Quiz 1').exists())

    def test_update_quiz(self):
        """Assure existing quiz is updated."""
        category = create_category(name="python")
        category_2 = create_category(name="javascript")
        quiz = create_quiz(name="quiz v1", category=category, creator=self.user_1)

        payload_data = {
            'name': 'quiz v2',
            'category_name': 'javascript'
        }

        response = self.client.put(reverse('quiz_detail', args=(quiz.id,)), data=payload_data)
        updated_quiz = Quiz.objects.get(id=quiz.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_quiz.name, "quiz v2")
        self.assertEqual(updated_quiz.category.name, "javascript")

    def test_update_quiz_by_non_creator(self):
        """Test non creat can't update someone else's quiz."""
        category = create_category(name='python')
        quiz = create_quiz(name="quiz v1", creator=self.user_2)

        payload_data = {
            'name': 'quiz v2',
            'category_name': 'python'
        }

        response = self.client.put(reverse('quiz_detail', args=(quiz.id,)), data=payload_data)
        quiz_obj = Quiz.objects.get(pk=quiz.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(quiz_obj.name, "quiz v1")

    def test_update_quiz_by_non_authenticated(self):
        """Test not logged in user can't update quiz."""
        quiz = create_quiz(name="quiz v1", creator=self.user_2)

        payload_data = {
            'name': 'quiz v2',
            'category_name': 'python'
        }

        self.client.logout()
        response = self.client.put(reverse('quiz_detail', args=(quiz.id,)), data=payload_data)
        quiz_obj = Quiz.objects.get(pk=quiz.id)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(quiz_obj.name, "quiz v1")

    def test_delete_quiz(self):
        """Assure specific quiz is removed."""
        quiz = create_quiz(name="quiz 1", creator=self.user_1)

        response = self.client.delete(reverse('quiz_detail', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Quiz.objects.count(), 0)

    def test_delete_quiz_by_non_authenticated(self):
        """Assure non authenticated user can't delete quiz."""
        quiz = create_quiz(name="quiz 1", creator=self.user_1)

        self.client.logout()
        response = self.client.delete(reverse('quiz_detail', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Quiz.objects.count(), 1)

    def test_delete_quiz_by_non_creator(self):
        """Assure non creator can't remove quiz from db."""
        quiz = create_quiz(name="quiz 1", creator=self.user_2)

        response = self.client.delete(reverse('quiz_detail', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Quiz.objects.count(), 1)

    def test_add_new_question_to_quiz(self):
        """Test add new question to existing quiz."""
        quiz = create_quiz(name="quiz 1", creator=self.user_1)

        payload_data = {
            'question': 'What is your name?',
            'explanation': 'Lorem ipsum ...',
            'answers': [
                dict(content='answer1', is_correct=False),
                dict(content='answer2', is_correct=True)
            ]
        }
        response = self.client.post(reverse('question_list', args=(quiz.id,)), data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Question.objects.get(question='What is your name?').quiz, quiz)
        self.assertEqual(QuestionAnswer.objects.count(), 2)

    def test_add_new_question_to_quiz_for_not_creator(self):
        """Test non creator, can't add new question for quiz."""
        quiz = create_quiz(name="quiz 1", creator=self.user_2)

        payload_data = {
            'question': 'What is your name?',
            'explanation': 'Lorem ipsum ...'
        }
        response = self.client.post(reverse('question_list', args=(quiz.id,)), data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Question.objects.count(), 0)

    def test_publish_quiz_by_creator(self):
        """Assure quiz is published."""
        quiz = create_quiz(name="Quiz 1", creator=self.user_1)

        response = self.client.post(reverse('quiz_publish', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['date_published'])

    def test_publish_quiz_by_non_creator(self):
        """Assure publishing quiz by non creator is forbiden."""
        quiz = create_quiz(name="Quiz 2", creator=self.user_2)

        response = self.client.post(reverse('quiz_publish', args=(quiz.id,)))
        quiz_obj = Quiz.objects.get(pk=quiz.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNone(quiz_obj.date_published)

    def test_unpublish_quiz_by_creator(self):
        """Assure quiz is unpublished"""
        quiz = create_quiz(name="Quiz 1", creator=self.user_1, date_published=timezone.now())

        response = self.client.post(reverse('quiz_unpublish', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(response.data['date_published'])

    def test_unpublish_quiz_by_non_creator(self):
        """Assure unpublishing quiz by non creator is not possible."""
        quiz = create_quiz(name="Quiz 2", creator=self.user_2, date_published=timezone.now())

        response = self.client.post(reverse('quiz_unpublish', args=(quiz.id,)))
        quiz_obj = Quiz.objects.get(pk=quiz.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(quiz_obj.date_published)


class TestQuestionDetail(APITestCase):
    """Test suit for question specific operations."""

    def setUp(self):
        self.user = create_user(username='user', password='password', email='email@gmail.com')
        self.user_2 = create_user(username='user2', password='password', email='email2@gmail.com')
        self.client.force_authenticate(user=self.user)

    def test_get_question_for_creator(self):
        """Test question detail is returned for creator."""
        quiz = create_quiz(name='name', creator=self.user)
        question = create_question(quiz=quiz, question='...', explanation='...')

        response = self.client.get(reverse('question_detail', args=(quiz.id, question.id)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], '...')

    def test_get_question_for_not_authenticated(self):
        """Make sure not authenticated user can't  access this endpoint."""
        quiz = create_quiz(name='name', creator=self.user)
        question = create_question(quiz=quiz, question='...', explanation='...')

        self.client.logout()
        response = self.client.get(reverse('question_detail', args=(quiz.id, question.id)))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_question_detail_for_not_author(self):
        """Assure questions detail is returned for not author."""
        quiz = create_quiz(name='name', creator=self.user_2, date_published=timezone.now())

        question = create_question(quiz=quiz, question='...', explanation='...')

        response = self.client.get(reverse('question_detail', args=(quiz.id, question.id)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['question'], '...')

    def test_update_question_by_author(self):
        """Assure author of quiz can update one of its questions."""
        quiz = create_quiz(name='name', creator=self.user)
        question = create_question(quiz=quiz, question='...', explanation='...')

        payload_data = {
            'question': 'New one ...',
            'explanation': 'changed explanation'
        }
        response = self.client.put(
            reverse('question_detail', args=(quiz.id, question.id)),
            data=payload_data)
        question_obj = Question.objects.get(pk=question.id)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(question_obj.question, "New one ...")
        self.assertEqual(response.data['question'], "New one ...")

    def test_update_question_not_author(self):
        """Assure only author can update question."""
        quiz = create_quiz(name='name', creator=self.user_2)
        question = create_question(quiz=quiz, question='...', explanation='...')

        payload_data = {
            'question': 'New one ...',
            'explanation': 'changed explanation'
        }
        response = self.client.put(
            reverse('question_detail', args=(quiz.id, question.id)),
            data=payload_data)
        question_obj = Question.objects.get(pk=question.id)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(question_obj.question, "...")

    def test_update_question_not_authenticated(self):
        """Make sure not authenticated user can't access this endpoint."""
        quiz = create_quiz(name='name', creator=self.user)
        question = create_question(quiz=quiz, question='...', explanation='...')

        payload_data = {
            'question': 'New one ...',
            'explanation': 'changed explanation'
        }
        self.client.logout()
        response = self.client.put(
            reverse('question_detail', args=(quiz.id, question.id)),
            data=payload_data)
        question_obj = Question.objects.get(pk=question.id)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(question_obj.question, "...")

    def test_update_question_with_answers(self):
        """
        Make sure question is updated, and new answers are added,
        old ones are destroyed.
        """
        quiz = create_quiz(name='quiz', creator=self.user)
        question = create_question(quiz=quiz, question='...', explanation='...')
        old_answer = create_question_answer(
            question=question, content='...', is_correct=True)

        payload_data = {
            'question': 'What is your name?',
            'explanation': 'Lorem ipsum ...',
            'answers': [
                dict(content='answer1', is_correct=False),
                dict(content='answer2', is_correct=True)
            ]
        }

        response = self.client.put(
            reverse('question_detail', args=(quiz.id, question.id)),
            data=payload_data
        )
        updated_obj = Question.objects.get(id=question.id)

        self.assertEqual(updated_obj.question, 'What is your name?')
        self.assertEqual(response.data, QuestionSerializer(updated_obj).data)
        self.assertEqual(QuestionAnswer.objects.count(), 2)
        self.assertEqual(updated_obj.answers.count(), 2)

    def test_delete_question_by_author(self):
        """Make sure user can delete question of his own quiz."""
        quiz = create_quiz(name='name', creator=self.user)
        question = create_question(quiz=quiz, question='...', explanation='...')

        response = self.client.delete(reverse('question_detail', args=(quiz.id, question.id)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Question.objects.count(), 0)

    def test_delete_question_by_non_creator(self):
        """Don't allow not quiz creator to delete question."""
        quiz = create_quiz(name='name', creator=self.user_2)
        question = create_question(quiz=quiz, question='...', explanation='...')

        response = self.client.delete(reverse('question_detail', args=(quiz.id, question.id)))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Question.objects.count(), 1)

    def test_delete_question_by_not_authenticated(self):
        """Make sure not authenticated user can't access this endpoint."""
        quiz = create_quiz(name='name', creator=self.user)
        question = create_question(quiz=quiz, question='...', explanation='...')

        self.client.logout()
        response = self.client.delete(reverse('question_detail', args=(quiz.id, question.id)))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Question.objects.count(), 1)


class TestQuizAvatar(APITestCase):
    """Test suite for avatar related actions for quiz."""

    def setUp(self):
        self.user = create_user(username='user', password='password', email='email1@gmail.com')
        self.user_2 = create_user(username='user2', password='password', email='email2@gmail.com')
        self.client.force_authenticate(self.user)

    def get_image_file(self, name, ext='png', size=(50, 50), color=(256, 0, 0)):
        file_obj = BytesIO()
        image = Image.new("RGBA", size=size, color=color)
        image.save(file_obj, ext)
        file_obj.seek(0)
        return File(file_obj, name=name)

    @mock.patch('mind_battle.storages.MediaRootS3Boto3Storage.save')
    def test_get_image_by_authenticated(self, mock_storage):
        """Assert any authenticated user can access quiz image."""
        mock_storage.return_value = 'image.png'
        image = self.get_image_file("image.png")
        quiz = create_quiz(
            name='Quiz 1',
            creator=self.user,
            image=image
        )

        response = self.client.get(reverse('quiz_image', args=(quiz.id,)), format='multipart')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['url'], quiz.image.url)

    @mock.patch('mind_battle.storages.MediaRootS3Boto3Storage.save')
    def test_uploading_image_by_creator(self, mock_storage):
        """Assert quiz image is uploaded by creator."""
        mock_storage.return_value = 'test.png'
        quiz = create_quiz(name='test', creator=self.user)
        image_to_upload = self.get_image_file("test.png")

        response = self.client.put(
            reverse('quiz_image', args=(quiz.id,)),
            data={'image': image_to_upload},
            format='multipart')
        quiz_obj = Quiz.objects.get(name='test')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(quiz_obj.image)

    def test_changing_image_by_not_creator(self):
        """Assert quiz image is not changed if not creator requested it."""
        quiz = create_quiz(name='test', creator=self.user_2)
        image_to_upload = self.get_image_file("sample.png")

        response = self.client.put(
            reverse('quiz_image', args=(quiz.id,)),
            data={'image': image_to_upload},
            format='multipart')
        quiz_obj = Quiz.objects.get(name='test')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(quiz_obj.image.name, 'default_quiz.jpeg')

    @mock.patch('mind_battle.storages.MediaRootS3Boto3Storage.save')
    def test_removing_image_by_creator(self, mock_storage):
        """Assert quiz image is removed if author requested it."""
        mock_storage.return_value = 'quiz-1.png'
        image = self.get_image_file("image.png")
        quiz = create_quiz(
            name='Quiz 1',
            creator=self.user,
            image=image
        )

        response = self.client.delete(reverse('quiz_image', args=(quiz.id,)))
        quiz_obj = Quiz.objects.get(name='Quiz 1')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(quiz_obj.image)

    @mock.patch('mind_battle.storages.MediaRootS3Boto3Storage.save')
    def test_removing_image_by_non_creator(self, mock_storage):
        """Make sure removing quiz image by non creator is not possible."""
        mock_storage.return_value = 'quiz-1.png'
        image = self.get_image_file("image.png")
        quiz = create_quiz(
            name='Quiz 1',
            creator=self.user_2,
            image=image
        )

        response = self.client.delete(reverse('quiz_image', args=(quiz.id,)))
        quiz_obj = Quiz.objects.get(name='Quiz 1')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(quiz_obj.image)


class TestCategory(APITestCase):
    """Test suite for Category model related actions."""

    def setUp(self):
        self.user = create_user(username='user', password='password', email='email@gmail.com')

    def test_create_new_category_by_authenticated(self):
        """Make sure authenticated user can create new category."""
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse("categories"), data={'name': 'New Category'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 1)

    def test_create_new_category_by_not_authenticated(self):
        """Make sure unauthenticated user can't create new category."""
        response = self.client.post(reverse("categories"), data={'name': 'new one'})

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Category.objects.count(), 0)

    def test_retrieve_category_list(self):
        """List of all cattegories is retrieved."""
        category_1 = create_category(name="first")
        category_2 = create_category(name="second")

        response = self.client.get(reverse('categories'))
        serialized_categories = CategorySerializer(Category.objects.all(), many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serialized_categories.data)
        self.assertIn(CategorySerializer(category_1).data, response.data)
