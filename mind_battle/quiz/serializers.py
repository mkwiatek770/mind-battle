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


class QuestionSerializer(serializers.ModelSerializer):
    quiz = QuizSerializer()

    class Meta:
        model = Question
        fields = ('quiz', 'question', 'explaination',
                  'good_answers', 'bad_answers')
