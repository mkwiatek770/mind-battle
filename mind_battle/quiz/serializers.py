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
    category = CategorySerializer(read_only=True)
    category_name = serializers.CharField(write_only=True)
    publish = serializers.BooleanField(write_only=True)

    def validate_category_name(self, value):
        """Check if category_name match with existing object in db."""
        if Category.objects.filter(name=value).exists():
            return value
        raise serializers.ValidationError("Category of given name does not exist")

    def create(self, validated_data) -> Quiz:
        """Create new quiz instance."""
        quiz = Quiz.objects.create(
            name=validated_data['name'],
            category=Category.objects.get(name=validated_data['category_name']),
            creator=self.context['request'].user
        )
        if validated_data['publish']:
            quiz.publish()
        return quiz

    def update():
        pass

    class Meta:
        model = Quiz
        fields = ('id', 'name', 'category', 'creator',
                  'date_created', 'date_published', 'date_modified',
                  'category_name', 'publish')
        read_only_fields = ('id', 'category', 'creator', 'date_created',
                            'date_published', 'date_modified')


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
