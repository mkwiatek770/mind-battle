from rest_framework import status
from rest_framework.test import APITestCase

from django.contrib.auth import get_user_model
from django.urls import reverse

from quiz.models import Quiz, Question, QuestionAnswer
from user.models import UserQuiz, UserAnswer


class TestUserQuiz(APITestCase):
    """Test suite for starting/finishing quiz by specific user."""

    def setUp(self):

        self.user = get_user_model().objects.create(
            username='user',
            password='password',
            email='email@gmail.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_start_quiz_by_authenticated(self):
        """Make sure authenticated user can start some quiz."""
        quiz = Quiz.objects.create(name='quiz')
        quiz.publish()

        response = self.client.post(reverse('quiz_start', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserQuiz.objects.count(), 1)

    def test_start_quiz_again(self):
        """Make sure user can start quiz again."""
        quiz = Quiz.objects.create(name='quiz')
        quiz.publish()
        quiz_user = UserQuiz.objects.create(quiz=quiz, user=self.user)

        date_started_before = quiz_user.date_started
        response = self.client.post(reverse('quiz_start', args=(quiz.id,)))
        modified_object = UserQuiz.objects.last()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserQuiz.objects.count(), 1)
        self.assertGreater(modified_object.date_started, date_started_before)
        self.assertIsNone(modified_object.date_finished)

    def test_start_unpublished_quiz(self):
        """Make sure user can't start unpublished quiz."""
        not_published_quiz = Quiz.objects.create(name='quiz')

        response = self.client.post(reverse('quiz_start', args=(not_published_quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(UserQuiz.objects.count(), 0)

    def test_finish_quiz_by_authenticated(self):
        """Make sure authenticated user can finish some quiz."""
        quiz = Quiz.objects.create(name='quiz')
        quiz.publish()
        UserQuiz.objects.create(quiz=quiz, user=self.user)

        response = self.client.post(reverse('quiz_finish', args=(quiz.id,)))
        modified_object = UserQuiz.objects.get(id=quiz.id)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertIsNotNone(modified_object.date_finished)

    def test_finish_unpublished_quiz(self):
        """Make sure user can't finish unpublished quiz."""
        quiz = Quiz.objects.create(name='quiz')

        response = self.client.post(reverse('quiz_finish', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_finish_not_started_quiz(self):
        """Make sure user can't finish unstarted quiz."""
        quiz = Quiz.objects.create(name='quiz')
        quiz.publish()

        response = self.client.post(reverse('quiz_finish', args=(quiz.id,)))

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class TestUserAnswer(APITestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(
            username='user',
            password='password',
            email='email@gmail.com'
        )
        self.client.force_authenticate(user=self.user)

    def test_answer_to_question_started_quiz(self):
        """Assert answering to one of quiz question that user started."""
        quiz = Quiz.objects.create(name='quiz')
        quiz.publish()
        question = Question.objects.create(question='Lorem ...', quiz=quiz, explanation='...')
        answer_1 = QuestionAnswer.objects.create(
            question=question, content='Answer 1', is_correct=True)
        answer_2 = QuestionAnswer.objects.create(
            question=question, content='Answer 2', is_correct=False)
        # start quiz
        quiz.start_quiz(self.user)

        payload_data = {
            'answer': answer_1.id
        }
        response = self.client.put(
            reverse('question_answer', args=(quiz.id, question.id)),
            data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(UserAnswer.objects.count(), 1)
        self.assertTrue(UserAnswer.objects.first().is_correct)

    def test_answer_to_question_not_started_quiz(self):
        """Forbid answering to not started quiz by user."""
        quiz = Quiz.objects.create(name='quiz')
        quiz.publish()
        question = Question.objects.create(question='Lorem ...', quiz=quiz, explanation='...')
        answer_1 = QuestionAnswer.objects.create(
            question=question, content='Answer 1', is_correct=True)
        answer_2 = QuestionAnswer.objects.create(
            question=question, content='Answer 2', is_correct=False)

        payload_data = {
            'answer': answer_1.id
        }
        response = self.client.put(
            reverse('question_answer', args=(quiz.id, question.id)),
            data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(UserAnswer.objects.count(), 0)

    def test_answer_to_question_for_finished_quiz(self):
        """Forbid user to answer to finished quiz."""
        quiz = Quiz.objects.create(name='quiz')
        quiz.publish()
        question = Question.objects.create(question='Lorem ...', quiz=quiz, explanation='...')
        answer_1 = QuestionAnswer.objects.create(
            question=question, content='Answer 1', is_correct=True)
        answer_2 = QuestionAnswer.objects.create(
            question=question, content='Answer 2', is_correct=False)
        quiz.start_quiz(self.user)
        quiz.finish_quiz(self.user)

        payload_data = {
            'answer': answer_1.id
        }
        response = self.client.put(
            reverse('question_answer', args=(quiz.id, question.id)),
            data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(UserAnswer.objects.count(), 0)

    def test_answer_to_question_by_unauthenticated(self):
        """Forbid answering to question if user is not authenticated."""
        quiz = Quiz.objects.create(name='quiz')
        quiz.publish()
        question = Question.objects.create(question='Lorem ...', quiz=quiz, explanation='...')
        answer_1 = QuestionAnswer.objects.create(
            question=question, content='Answer 1', is_correct=True)
        answer_2 = QuestionAnswer.objects.create(
            question=question, content='Answer 2', is_correct=False)
        quiz.start_quiz(self.user)

        payload_data = {
            'answer': answer_1.id
        }
        # logout user
        self.client.logout()
        response = self.client.put(
            reverse('question_answer', args=(quiz.id, question.id)),
            data=payload_data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(UserAnswer.objects.count(), 0)

    def test_answer_to_all_questions_by_authenticated(self):
        """Make sure authenticated user can answer to all questions."""
        quiz = Quiz.objects.create(name='Quiz1')
        quiz_user = UserQuiz.objects.create(quiz=quiz, user=self.user)
        quiz.publish()
        question_1 = Question.objects.create(question='q1', quiz=quiz, explanation='...')
        question_2 = Question.objects.create(question='q2', quiz=quiz, explanation='...')
        answer_1_1 = QuestionAnswer.objects.create(
            question=question_1, content='Answer 1', is_correct=True)
        answer_1_2 = QuestionAnswer.objects.create(
            question=question_1, content='Answer 2', is_correct=False)
        answer_2_1 = QuestionAnswer.objects.create(
            question=question_2, content='Answer 3', is_correct=True)
        answer_2_2 = QuestionAnswer.objects.create(
            question=question_2, content='Answer 4', is_correct=False)

        payload_data = {
            'answers': [
                {'answer_id': answer_1_1.id, 'question_id': question_1.id},
                {'answer_id': answer_2_2.id, 'question_id': question_2.id}
            ]
        }

        response = self.client.post(
            reverse('user_answer', args=(quiz.id,)),
            data=payload_data
        )

        self.assertEqual(response.status_code, 204)
        self.assertEqual(UserAnswer.objects.count(), 2)

    def test_answer_to_all_questions_by_not_authenticated(self):
        """Make sure anonymous user can't answer to all questions."""
        quiz = Quiz.objects.create(name='Quiz1')
        quiz_user = UserQuiz.objects.create(quiz=quiz, user=self.user)
        quiz.publish()
        question_1 = Question.objects.create(question='q1', quiz=quiz, explanation='...')
        question_2 = Question.objects.create(question='q2', quiz=quiz, explanation='...')
        answer_1_1 = QuestionAnswer.objects.create(
            question=question_1, content='Answer 1', is_correct=True)
        answer_2_1 = QuestionAnswer.objects.create(
            question=question_2, content='Answer 3', is_correct=True)

        payload_data = {
            'answers': [
                {'answer_id': answer_1_1.id, 'question_id': question_1.id},
                {'answer_id': answer_2_1.id, 'question_id': question_2.id}
            ]
        }

        self.client.logout()
        response = self.client.post(
            reverse('user_answer', args=(quiz.id,)),
            data=payload_data
        )

        self.assertEqual(response.status_code, 401)
        self.assertEqual(UserAnswer.objects.count(), 0)

    def test_answer_to_all_questions_quiz_not_started(self):
        """Assert user can't answer to questions for not started quiz."""
        pass

    def test_answer_to_questions_unpublished_quiz(self):
        """Make sure user can't answer to questions if quiz is unpublished."""
        pass

    def test_answer_to_questions_invalid_answers(self):
        """Test 400 bad request is raised on invalid answer ids."""
        pass
