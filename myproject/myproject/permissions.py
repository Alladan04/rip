from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser

from app.models import UserProfile

import redis # type: ignore
from myproject.settings import REDIS_HOST, REDIS_PORT


session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

class IsManager(BasePermission):
    def has_permission(self, request, view):
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return False
        
        user = UserProfile.objects.get(username=session_storage.get(ssid).decode('utf-8'))
        return  user.is_staff
'''
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        try:
            ssid = request.COOKIES["session_id"]
        except:
            return False
        
        user = UserProfile.objects.get(username=session_storage.get(ssid).decode('utf-8'))
        return user.is_superuser
'''

def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes        
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator