from rest_framework import authentication
from rest_framework import exceptions
from rest_framework import status
from user.models import User
from user.serializers import UserSerializer


class QuizAuthentication(authentication.BaseAuthentication):
    """
    Custom authentication backend.
    """

    def authenticate(self, request):

        if not request.data.get('username'):
            return None  # no username passed in request data

        try:
            user = User.objects.get(username=request.data['username'])
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(
                "User does not exist.",
                code=status.HTTP_403_FORBIDDEN
            )

        # Check password
        if not user.check_password(request.data['password']):
            raise exceptions.AuthenticationFailed(
                "Invalid password.",
                code=status.HTTP_403_FORBIDDEN
            )

        return (user, None)  # Authentication successful
