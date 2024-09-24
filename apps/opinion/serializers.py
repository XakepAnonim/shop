from typing import Any

from rest_framework import serializers

from .models import Opinion, Grades


class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = ['title', 'grade']


class OpinionSerializer(serializers.ModelSerializer):
    grades = GradesSerializer(many=True)
    total_likes = serializers.SerializerMethodField()

    def get_total_likes(self, obj: Opinion) -> int:
        return obj.total_likes

    def create(self, validated_data: dict[str, Any]) -> Opinion:
        grades_data = validated_data.pop('grades')
        opinion = Opinion.objects.create(**validated_data)
        for grade_data in grades_data:
            Grades.objects.create(opinion=opinion, **grade_data)
        return opinion

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
        ]


class OpinionCommentSerializer(serializers.ModelSerializer):
    grades = GradesSerializer(many=True)
    total_likes = serializers.SerializerMethodField()

    def get_total_likes(self, obj: Opinion) -> int:
        return obj.total_likes

    def create(self, validated_data: dict[str, Any]) -> Opinion:
        grades_data = validated_data.pop('grades')
        opinion = Opinion.objects.create(**validated_data)
        for grade_data in grades_data:
            Grades.objects.create(opinion=opinion, **grade_data)
        return opinion

    class Meta:
        model = Opinion
        fields = [
            'uuid',
            'user',
            'text',
            'opinion',
            'total_likes',
        ]
