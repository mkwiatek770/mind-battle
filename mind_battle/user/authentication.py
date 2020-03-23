from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import status
from django.contrib.auth import get_user_model
from user.serializers import UserSerializer


class QuizAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication backend.
    """

    def authenticate(self, request):

        if not request.data.get('username'):
            return None  # no username passed in request data

        try:
            user = get_user_model().objects.get(username=request.data['username'])
        except get_user_model().DoesNotExist:
            return None
        # Check password
        if not user.check_password(request.data['password']):
            raise exceptions.AuthenticationFailed(
                "Invalid password.",
                code=status.HTTP_403_FORBIDDEN
            )

        return (user, None)  # Authentication successful

    def get_user(user_id: int):
        try:
            return get_user_model().objects.get(id=user_id)
        except get_user_model().DoesNotExist:
            return None
