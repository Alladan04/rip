from rest_framework.response import Response
from ..models import UserProfile, OperationRequest, Request
from rest_framework import status
from myproject.settings import REDIS_HOST, REDIS_PORT
import redis
session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
def get_session(request):
    ssid = request.COOKIES.get("session_id")

    if ssid is None:
        ssid = request.headers.get("authorization")
    return ssid

def get_us_id(request):
        try:
            ssid = get_session(request)#request.COOKIES["session_id"]
        except:
            return None#Response(status=status.HTTP_403_FORBIDDEN)

        return UserProfile.objects.get(username=session_storage.get(ssid).decode('utf-8'))
def operation_util( req: Request):
    item = OperationRequest.objects.filter(request = req)
    for i in item:
        a = i.operand1
        b = i.operand2
        if (a == None):
            a = 0
        if (b== None):
            b = 0
        match i.operation.id:
            case 1:
                i.result = a|b
            case 2:
                i.result = a&b
            case 3:
                i.result = a^b
            case 4:
                i.result = ~(a|b)
            case 5:
                i.result = ~(a&b)
            case 6:
                i.result = ~a
        i.save()
    return req