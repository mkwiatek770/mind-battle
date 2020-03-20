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
    publish = serializers.BooleanField(write_only=True, required=False)

    def validate_category_name(self, value) -> str:
        """Check if category_name match with existing object in db."""
        if Category.objects.filter(name=value).exists():
            return value
        raise serializers.ValidationError("Category of given name does not exist")

    def validate(self, data):
        """Make sure that user is in request context."""
        if self.context['request'].user.is_anonymous:
            raise serializers.ValidationError("User is anonymous")
        return data

    def create(self, validated_data) -> Quiz:
        """Create new quiz instance."""
        quiz = Quiz.objects.create(
            name=validated_data['name'],
            category=Category.objects.get(name=validated_data['category_name']),
            creator=self.context['request'].user
        )
        if validated_data.get('publish'):
            quiz.publish()
        return quiz

    def update(self, instance, validated_data):
        """Update existing quiz instance."""
        if validated_data.get("publish"):
            instance.publish()
        elif validated_data.get("publish") is False:
            instance.unpublish()
        if not instance.category or validated_data["category_name"] != instance.category.name:
            category = Category.objects.get(name=validated_data["category_name"])
            instance.category = category
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance

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
