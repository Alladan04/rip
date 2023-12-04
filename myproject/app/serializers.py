from .models import Operation, Request, OperationRequest,UserProfile
from rest_framework import serializers
from collections import OrderedDict
class OperationSerializer(serializers.ModelSerializer):
    image = serializers.CharField(default = "")
    class Meta:
       
        # Модель, которую мы сериализуем
        model = Operation
        # Поля, которые мы сериализуем
        fields = ["name", "status", "type", "description","pk","img", "image"]
        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 
'''
class OrderResponse(serializers.Serializer):
    data = OperationSerializer(many = True)
    request_id = serializers.IntegerField()
'''

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
        model = UserProfile
        fields = ['password', 'is_staff', 'username', 'email', 'id']


'''
class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Request
        fields = ['status']
class Operands(serializers.ModelSerializer):
    class Meta:
        model = OperationRequest
        fields = ['operand1', 'operand2']
'''
'''
################Schemas##################

class PostOperationSchema(serializers.Serializer):
    data = OperationSerializer(many = False)
class OperationsResponseSchema(serializers.Serializer):
    data = OperationSerializer(many = True, read_only = True)
    request_id = serializers.IntegerField()
    '''