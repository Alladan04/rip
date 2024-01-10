from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

from app.models import UserProfile

import redis # type: ignore
from myproject.settings import REDIS_HOST, REDIS_PORT
#from ..app.views.utils import get_session

session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
def get_session(request):
    ssid = request.COOKIES.get("session_id")

    if ssid is None:
        ssid = request.headers.get("authorization")
    return ssid
class IsManager(BasePermission):
    def has_permission(self, request, view):
        try:
            ssid = get_session(request)#request.COOKIES["session_id"]
        except:
            return False
        
        user = UserProfile.objects.get(username=session_storage.get(ssid).decode('utf-8'))
        return  user.is_staff or user.is_superuser

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            ssid = get_session(request) #request.COOKIES["session_id"]
        except:
            return False
        
        user = UserProfile.objects.get(username=session_storage.get(ssid).decode('utf-8'))
        return user.is_superuser


class IsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        try:
            ssid = get_session(request)#request.COOKIES.get("session_id")
            '''if ssid is None:
                ssid = request.headers.get("authorization")
            print(request.headers.get("authorization"))'''
            if ssid is None:
                return False
        except Exception as e:
            return False

        if session_storage.get(ssid):
            user = UserProfile.objects.get(username=session_storage.get(ssid).decode('utf-8'))
            return user.is_active

        return False
def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes        
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator