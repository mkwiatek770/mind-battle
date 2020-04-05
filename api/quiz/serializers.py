from typing import List
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
        read_only_fields = ('id',)


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

    def update(self, instance, validated_data) -> Quiz:
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
                  'category_name', 'publish', 'image')
        read_only_fields = ('id', 'category', 'creator', 'date_created',
                            'date_published', 'date_modified', 'image')


class QuestionAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = QuestionAnswer
        fields = ('id', 'content', 'is_correct')


class QuestionSerializer(serializers.ModelSerializer):

    answers = QuestionAnswerSerializer(many=True, required=False)

    def create(self, validated_data) -> Question:
        """Create question instance."""
        answers = validated_data.pop('answers')
        quiz = Quiz.objects.get(pk=self.context['quiz_pk'])
        question = Question.objects.create(quiz=quiz, **validated_data)

        QuestionAnswer.objects.bulk_create([
            QuestionAnswer(**answer, question=question) for answer in answers
        ])
        return question

    def update(self, instance, validated_data) -> Question:
        """Update question instance."""
        instance.question = validated_data['question']
        instance.explanation = validated_data['explanation']

        if validated_data.get('answers'):
            instance.answers.filter().delete()
            QuestionAnswer.objects.bulk_create(
                [QuestionAnswer(**answer, question=instance) for answer in validated_data['answers']])

        instance.save()
        return instance

    # def update(self, quiz_istance, validated_data) -> Question:
    #     """Update question instance for specific quiz."""
    #     answers = validated_data.pop('answers')
    #     question = Question.objects.create(
    #         quiz=quiz_istance,
    #         **validated_data
    #     )
    #     for answer in answers:
    #         question.answers.filter().delete()
    #         QuestionAnswer.objects.bulk_create(
    #             [QuestionAnswer(**answer, question=instance)
    #              for answer in validated_data['answers']]
    #         )
    #     return question

    class Meta:
        model = Question
        fields = ('id', 'question', 'answers', 'explanation',)
        read_only_fields = ('id', 'answers')


class ImageSerializer(serializers.Serializer):

    url = serializers.CharField(read_only=True)
    image = serializers.ImageField(write_only=True)

    def get_full_path(self):
        pass

    def update(self, instance, validated_data):
        quiz = Quiz.objects.get(pk=self.context['quiz_pk'])
        quiz.image = validated_data['image']
        quiz.save()
        return quiz
