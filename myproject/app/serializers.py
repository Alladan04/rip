from .models import Operation
from rest_framework import serializers


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Operation
        # Поля, которые мы сериализуем
        fields = ["name", "status", "type", "description"]