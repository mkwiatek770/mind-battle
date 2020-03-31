from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.utils.text import gettext_lazy
from user.models import User, QuestionUser
from quiz.models import QuestionAnswer, Question


class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)

    def create(self, validated_data: dict) -> User:
        validated_data.pop('re_password')
        user = User.objects.create_user(**validated_data)
        return user

    def validate(self, data: dict) -> dict:
        if not data['re_password'] == data['password']:
            raise serializers.ValidationError("Passwords don't match.")
        return data

    def validate_age(self, value: int) -> int:
        if value <= 13:
            raise ValueError("You're too young to register.")
        return value

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 're_password', 'email', 'age')
        read_only_fields = ('id',)


class RefreshTokenSerializer(serializers.Serializer):

    refresh = serializers.CharField()

    default_error_message = {
        'bad_token': gettext_lazy('Token is invalid or expired')
    }

    def validate(self, data):
        self.token = data['refresh']
        return data

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


class UserAnswersSerializer(serializers.Serializer):

    answers = serializers.ListField()

    def create(self, validated_data):

        user_answers = []
        for answer in validated_data['answers']:
            question = Question.objects.get(id=answer['question_id'])
            answer = QuestionAnswer.objects.get(id=answer['answer_id'])
            user_answers.append(QuestionUser(question=question, answer=answer,
                                             user=self.context['request'].user))
        return QuestionUser.objects.bulk_create(user_answers)
