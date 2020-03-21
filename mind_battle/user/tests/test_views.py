from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model


class TestUserQuiz(APITestCase):
    """Test suite for starting/finishing quiz by specific user."""

    def setUp(self):

        self.user = get_user_model().objects.create(
            username='user',
            password='password'
        )
        self.client.force_authenticate(user=self.user)

    def test_start_quiz_by_authenticated(self):
        """Make sure authenticated user can start some quiz."""
        pass

    def test_start_quiz_again(self):
        """Make sure user can start quiz again."""
        pass

    def test_start_unpublished_quiz(self):
        """Make sure user can't start unpublished quiz."""
        pass

    def test_finish_quiz_by_authenticated(self):
        """Make sure authenticated user can finish some quiz."""
        pass

    def test_finish_unpublished_quiz(self):
        """Make sure user can't finish unpublished quiz."""
        pass

    def test_finish_not_started_quiz(self):
        """Make sure user can't finish unstarted quiz."""
        pass


class TestUserAnswer(APITestCase):

    def setUp(self):

        self.user = get_user_model().objects.create(
            username='user',
            password='password'
        )
        self.client.force_authenticate(user=self.user)

    def test_answer_to_question_started_quiz(self):
        """Assert answering to one of quiz question that user started."""
        pass

    def test_answer_to_question_not_started_quiz(self):
        """Forbid answering to not started quiz by user."""
        pass

    def test_answer_to_question_by_authenticated(self):
        """Forbid answering to question if user is not authenticated."""
        pass
