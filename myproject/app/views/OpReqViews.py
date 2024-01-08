from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import psycopg2
from datetime import date
from django.http import UnreadablePostError
from ..serializers import  OperationRequestSerializer
from ..models import Operation,OperationRequest,Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions as rest_permissions
import datetime
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from  rest_framework.exceptions import bad_request
import requests as python_requests
import json
from myproject.permissions import *
from myproject.settings import REDIS_HOST, REDIS_PORT
from rest_framework import status as r_status
from drf_yasg.utils import swagger_auto_schema
import redis
from .utils import get_us_id
session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)
class OperationRequestView(APIView):
    #permission_classes=[rest_permissions.IsAuthenticated]
    @method_permission_classes([IsAuthenticated,])
    def delete(self, request, id):
        '''
        Удалить операцию из заявки, доступно только авторизованным пользователям'''
        #ТУТ наверно стоит вернуть гет из Реквест по реквест_ид из м-м
        #Но как это сделать?(
        '''try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=r_status.HTTP_403_FORBIDDEN)'''
        #user_id= UserProfile.objects.get(username=session_storage.get(ssid).decode('utf-8')).id
        #current_request = Request.objects.filter(user=user_id, breach_status='введён')
        #if current_request.exists():  
        user = get_us_id(request=request) 
        try:
            op_req = OperationRequest.objects.get(id = id)
            if (op_req):
                req = op_req.request
                if (req.status != "введён"):
                    return Response(status=r_status.HTTP_400_BAD_REQUEST, data = "You cant change the sent request")
                op = op_req.operation
                if req.user == user: 
                    op_req.delete()
                    return Response(status = r_status.HTTP_200_OK, data ='Deleted operation #{op} from request#{req}'.format(req = req, op=op))
                else:
                    return Response(status = r_status.HTTP_403_FORBIDDEN)
        except:
            return Response(status = 400, data = 'Bad request. Probably the id you are referring to does not exist')
        return Response (status = 400, data = 'Something went wrong')
    
    @swagger_auto_schema(request_body=OperationRequestSerializer)
    @method_permission_classes([IsAuthenticated,])
    def put(self, request, id): #change operands
        '''
        Изменение операндов в м-м, доступно только авторзованным пользователям
        если подать ИД заявки, которая уже в работе/удалена/завершена/отменена, то вернет 400
        если подать невалидное тело запроса, вернет 400, 
        если подать ИД м-м, который не существует,то вернет 400
        иначе изменит операнд и вернет новое значение м-м'''
        user = get_us_id(request=request)
        try:
            try:
               operation_r = OperationRequest.objects.filter(id=id)[0]
            except:
               return Response(status = r_status.HTTP_404_NOT_FOUND)
            if operation_r.request.status =='введён'and operation_r.request.user == user:
                serializer = OperationRequestSerializer(operation_r, data = request.data['data'], partial = True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'data':serializer.data})
            else:
                return Response(status = r_status.HTTP_403_FORBIDDEN, data = "Error while trying to change")
        except:
            return Response(status = 400, data = 'Bad request. Probably wrong request body or id')
