from rest_framework import serializers

from apps.main.models import Brand


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = [
            'uuid',
            'name',
        ]
