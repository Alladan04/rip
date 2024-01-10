from rest_framework.response import Response

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
#from requests import Response
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework import permissions
from ..models import UserProfile
from .utils import get_session
from ..serializers import UserSerializer
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import api_view, permission_classes, authentication_classes
import uuid
import redis # type: ignore
from myproject.settings import REDIS_HOST, REDIS_PORT
from datetime import timedelta
from myproject.permissions import IsManager, method_permission_classes
session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

'''
class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and (request.user.is_staff ))
    
def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes        
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator
'''
class UserViewSet(viewsets.ModelViewSet):
    """Класс, описывающий методы работы с пользователями
    Осуществляет связь с таблицей пользователей в базе данных
    """
    queryset = UserProfile.objects.all()
    serializer_class = UserSerializer
    model_class = UserProfile

    def get_permissions(self):
    
        if self.action in ['create']:
            permission_classes = [AllowAny]
        elif self.action in ['list']:
            permission_classes = [IsManager]
       
        return [permission() for permission in permission_classes]
    def get(self, request):
        '''Только ддля тестирования'''
        users = UserProfile.all()
        serialized_data= UserSerializer(users,many = True)
        return Response(status=200, data =serialized_data )
    def create(self, request):
        """
        Функция регистрации новых пользователей
        Если пользователя c указанным в request email ещё нет, в БД будет добавлен новый пользователь.
        """
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            self.model_class.objects.create_user(email=serializer.data['email'],
                                     username = serializer.data['username'],
                                     password=serializer.data['password'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            return Response({'status': 'Success'}, status=200)
        return Response(data= serializer._errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['Post'])
@permission_classes([AllowAny])
def check_auth(request):
    #session_id = request.COOKIES["session_id"]#request.headers.get("authorization")
    session_id = get_session(request=request)
    print(session_id)

    print(session_storage.get(session_id))

    if (session_storage.get(session_id)):
        user = UserProfile.objects.get(username=session_storage.get(session_id).decode('utf-8'))
        
        serializer = UserSerializer(user, many=False)
        print(serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_403_FORBIDDEN)


@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
def login_view(request):
    print(request.data)
    username= request.data["username"]
    password = request.data["password"]
    #print(UserProfile.objects.all()[0])
    user = authenticate(request, username=username, password=password)#ходит в бдшку  и чекает
    if user is not None:
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)

        print(user.last_login)
        print(user.get_username())

        data = {
            "session_id": random_key,
            "user_id": user.pk,
            "username": user.username,
            "password":user.password,
            "is_staff":user.is_staff
        }

        response = Response(data, status=status.HTTP_201_CREATED)
        response.set_cookie("session_id", random_key, httponly=False, expires=timedelta(days=1))


        return response
    else:
        return Response (data = "failed",status = status.HTTP_403_FORBIDDEN) #("{'status': 'error', 'error': 'login failed'}")



#@csrf_exempt
@swagger_auto_schema(method='post')
@api_view(['Post'])
@permission_classes([AllowAny])
def logout_view(request):
    try:
       ssid = get_session(request=request) #request.headers.get("authorization")
       #ssid = request.COOKIES["session_id"]
       print(ssid)
    except:
        return Response(data = 'logout failed',status = status.HTTP_403_FORBIDDEN)#HttpResponse("{'status': 'error', 'error': 'logout failed'}")
        
    session_storage.delete(ssid)

    logout(request._request)
    response = Response(status = status.HTTP_200_OK)
    response.delete_cookie("session_id")
    return response