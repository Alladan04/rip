from .models import Operation, Request, OperationRequest,User
from rest_framework import serializers


class OperationSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Operation
        # Поля, которые мы сериализуем
        fields = ["name", "status", "type", "description","pk"]

class RequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = '__all__'

class OperationRequestSerializer (serializers.ModelSerializer):
    class Meta:
        model = OperationRequest
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'