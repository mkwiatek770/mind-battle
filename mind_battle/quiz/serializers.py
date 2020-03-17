from rest_framework import serializers
from quiz.models import (
    Quiz,
    Question,
    QuestionAnswer,
    Category
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')


class QuizSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Quiz
        fields = ('id', 'name', 'category', 'creator',
                  'date_created', 'date_published', 'date_modified')


class QuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswer
        fields = ('id', 'content', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()
    answers = QuestionAnswerSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'quiz', 'question', 'answers', 'explaination',
                  'good_answers', 'bad_answers')
