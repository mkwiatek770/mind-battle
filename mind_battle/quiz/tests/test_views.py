""""Test endpoints for API."""
import unittest
from rest_framework.test import APIRequestFactory


class TestQuizUnauthenticated(unittest.TestCase):
    """Test for quiz related endpoints for unathenticated user."""

    def setUp(self):
        self.request = APIRequestFactory()

    def test_get_all_published_quizzes(self):
        """Get all quizzes that was already published"""
        pass

    def test_get_quizes_of_category(self):
        """Receive all quizzes by given category."""
        pass

    def test_get_quiz_detail(self):
        """Receive detail info about specific quiz."""
        pass

    def test_get_quiz_questions(self):
        """Receive list of questions for specific quiz."""
        pass

    def test_answer_to_question(self):
        """Submit answer to specific quiz question."""
        pass

    def test_change_answer_to_question(self):
        """Change already submitted answer."""
        pass


class TestQuizAuthenticated(unittest.TestCase):
    """Test for quiz related endpoints for unathenticated user."""

    def setUp(self):
        self.request = APIRequestFactory()

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
