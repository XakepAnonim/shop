from typing import Any

from rest_framework import serializers

from apps.opinion.models import Grades, Opinion, Comment, Question


class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = ['title', 'grade']


class OpinionSerializer(serializers.ModelSerializer):
    grades = GradesSerializer(many=True)

    def create(self, validated_data: dict[str, Any]) -> Opinion:
        grades_data = validated_data.pop('grades')
        opinion = Opinion.objects.create(
            user=self.context['user'],
            product=self.context['product'],
            **validated_data,
        )
        for grade_data in grades_data:
            Grades.objects.get(opinion=opinion, **grade_data)
        return opinion

    class Meta:
        model = Opinion
        fields = [
            'advantages',
            'disadvantages',
            'commentary',
            'problem',
            'images',
            'periods',
            'grades',
        ]


class GetOpinionSerializer(serializers.ModelSerializer):
    grades = GradesSerializer(many=True)
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj: Opinion) -> dict:
        comment = obj.comments.first()
        if comment:
            serializer = CommentSerializer(comment)
            return serializer.data

    class Meta:
        model = Opinion
        fields = [
            'user',
            'product',
            'advantages',
            'disadvantages',
            'commentary',
            'problem',
            'images',
            'periods',
            'grades',
            'total_likes',
            'comments',
        ]


class CommentSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict[str, Any]) -> Comment:
        opinion = self.context.get('opinion')
        question = self.context.get('question')
        comment = None

        if opinion:
            comment = Comment.objects.create(
                user=self.context['user'],
                opinion=self.context['opinion'],
                **validated_data,
            )
        elif question:
            comment = Comment.objects.create(
                user=self.context['user'],
                question=self.context['question'],
                **validated_data,
            )
        return comment

    class Meta:
        model = Comment
        fields = [
            'text',
        ]


class GetCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = [
            'uuid',
            'user',
            'text',
            'total_likes',
        ]


class QuestionSerializer(serializers.ModelSerializer):
    def create(self, validated_data: dict[str, Any]) -> Opinion:
        question = Question.objects.create(
            user=self.context['user'],
            product=self.context['product'],
            **validated_data,
        )
        return question

    class Meta:
        model = Question
        fields = [
            'title',
            'text',
        ]


class GetQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = [
            'uuid',
            'user',
            'text',
            'total_likes',
        ]
