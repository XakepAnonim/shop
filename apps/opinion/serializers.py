from rest_framework import serializers
from .models import Opinion, Grades


class GradesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grades
        fields = ['title', 'grade']


class OpinionSerializer(serializers.ModelSerializer):
    grades = GradesSerializer(many=True)

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
        ]
