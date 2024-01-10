from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import psycopg2
from datetime import date
from django.http import UnreadablePostError
from ..serializers import OperationSerializer, OperationRequestSerializer,RequestSerializer
from ..models import Operation,OperationRequest,Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions as rest_permissions
from myproject.permissions import *
from myproject.settings import REDIS_HOST, REDIS_PORT
from .conf import BASE_IMG
import redis
import datetime
from rest_framework.decorators import api_view,permission_classes
from  rest_framework.exceptions import bad_request
import requests as python_requests
import json
from rest_framework import status as r_status
from .filters import RequestFilter
from .OperationViews import getImage
from drf_yasg.utils import swagger_auto_schema
from .utils import get_us_id, operation_util
import pytz
from django.views.decorators.csrf import csrf_exempt
import requests
#session_storage = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)

def get_adm_id():
    return 2
def getUsername(id):
    return UserProfile.objects.get(id = id).username
class RequestListView(APIView):
    #permission_classes=[rest_permissions.IsAuthenticated]
    @method_permission_classes([IsAuthenticated,])
    def get(self, request, format = None):
        '''по юзер_ид выдает список заявок, есть фильтрация по статусу заявки.
        фильтры устанавливаются в квери параметрах урла в виде
        status_list=статус1|статус2...и т.д.
        если передан статус, которого не существует, возвращает бэд реквест'''
        try:
            user_id = get_us_id(request=request).id
        except:
            return Response(status=r_status.HTTP_401_UNAUTHORIZED)
        user = UserProfile.objects.get(id = user_id)
        requests = RequestFilter(Request.objects,request, user)
        try:
            serialized_list = [RequestSerializer(request).data for request in requests]
            #plus_user = [{"item":item, "user":"allochka"} for item in serialized_list]
            for item in serialized_list:
                item["user"]= getUsername(item["user"])
                if item["admin"]:
                    item["admin"] = getUsername(item["admin"])
                #item["admin"] = getUsername(item["admin"])
            #serialized_list = [request["username"] = getUsername(request["user_id"]) for request in serialized_list]
            return Response(data= {'data':serialized_list})
        except:
            return Response( status = 400, data = "Bad Request")
   
class RequestView(APIView):
   # permission_classes = [rest_permissions.IsAuthenticated]
    @method_permission_classes([IsAuthenticated,]) 
    def get (self, request,id):
        ''' 
        Просмотр одной заявки, доступно только авторизованным пользователям
        возвращает заявку по ИД вместе со всеми услугами, которые в нее включены и их подробной информацией
        (возможно, это избыточно, и было бы достаточно вернуть элемент из м-м, ссылающийся на саму услугу по ключу)
        Если введен ИД несуществующей заявки, возвращает бэд реквест'''
        '''try:
            ssid = request.COOKIES["session_id"]
        except:
            return Response(status=r_status.HTTP_403_FORBIDDEN)
        user = UserProfile.objects.get(username = session_storage.get(ssid).decode('utf-8'))'''
        user = get_us_id(request=request)
        if not user.is_staff and not user.is_superuser:
            ob_request = Request.objects.filter(id = id, user = user)
            if ob_request.exists():
                opreqs = OperationRequest.objects.filter(request = ob_request[0])
            else:
                return Response(status = r_status.HTTP_404_NOT_FOUND)
        else:    
            ob_request = Request.objects.filter(id = id)
            if ob_request.exists():
                ob_request=ob_request[0]
            else:
                return Response(status = r_status.HTTP_404_NOT_FOUND)
            opreqs= OperationRequest.objects.filter(request = ob_request)
        try:
            serialized_opreq = [OperationRequestSerializer(opreq).data for opreq in opreqs]
            for i in serialized_opreq:
                url= "http://127.0.0.1:8000/operation/"+str(i['operation'])
                i['operation'] = OperationSerializer(Operation.objects.get(id = i['operation'])).data
                if (i['operation']['img']!=None):
                    i['operation']['image'] = getImage(i['operation']['img'])
                else:
                    i['operation']['image'] = getImage(BASE_IMG)
            serialized_request= RequestSerializer(ob_request).data
            return Response(data = {'data':{'request':serialized_request, 'items':serialized_opreq}})#'operations':serialized_operations}})
        except:
            return Response(status=400, data = "Bad Request. Probably the request you are referring to does not exist") 
    @method_permission_classes([IsAuthenticated,])
    def delete(self,request,id):
        '''
        Удалить заявку, доступно только авторизованным пользователям.
        меняет статус выбранной заявки текущего юзера на удалён
        потом удаляет все связанные элементы из м-м физически
        если подали ИД который не существует, возвращает бэд реквест'''
        try:
            user_id = get_us_id(request=request) #get_us_id()
            ob_request = Request.objects.filter(id =id, user = user_id)[0]
            ob_request.status = 'удалён'
            ob_request.finish_date = datetime.datetime.now(tz=pytz.UTC)
            ob_request.save()
            op_reqs = OperationRequest.objects.filter(request = ob_request)
            for op_req in op_reqs:
                op_req.delete()
                #ЧТО ВОЗВРАЩАТЬ??
            return Response(status = r_status.HTTP_200_OK, data = 'Deleted request #{n} '.format(n = id))
        except:
            return Response(status = 400, data = 'Bad request. Probably the request you are referring to does not exist')
        
    @method_permission_classes((IsManager,))
    def put(self,request, id):
        '''
        Завершение заявки (выполнение или отклонение).Доступно только авторизованному модератору.
        '''
        admin_id = get_us_id(request) #get_adm_id()
        #тут менять по ИД заявки или по ИД юзера?\
        try:
            status= request.data['data']['status']
        except:
            return Response(status = r_status.HTTP_400_BAD_REQUEST)
        if not status in ['отменён', 'завершён']:
            return Response(status = r_status.HTTP_400_BAD_REQUEST)
        try:
            req = Request.objects.filter(id = id, status = 'в работе')[0]
        except:
            return  Response(status = r_status.HTTP_404_NOT_FOUND, data = 'no such id or the status does not match or the admin is not set')
        if status == 'завершён':
            operation_util(req)
        req.status = status
        req.admin= admin_id
        req.finish_date = datetime.datetime.now(tz=pytz.UTC)
        req.save()
        return Response(status = r_status.HTTP_200_OK, data ={'data': RequestSerializer(req).data})
    


@swagger_auto_schema(method='put', request_body= RequestSerializer)  
@api_view(['Put'])
@permission_classes([IsAuthenticated])
#@method_permission_classes([IsAuthenticated,]) 
def form(request, id):
    user_id = get_us_id(request=request)
    #тут менять по ИД заявки
    try:
        req = Request.objects.filter(id = id, user = user_id, status = 'введён')[0]
    except:
        return Response(status = r_status.HTTP_400_BAD_REQUEST, data = 'Something got wrong')
    req.status = 'в работе'
    req.form_date = datetime.datetime.now(tz=pytz.UTC)
    req.save()
    return Response(status = r_status.HTTP_200_OK, data ={'data': RequestSerializer(req).data})



'''
@method_permission_classes(IsManager)          
@swagger_auto_schema(method = 'put',request_body=RequestSerializer)
@api_view(['Put'])
def decline_accept(request, id):
    
    admin_id = get_us_id(request) #get_adm_id()
    #тут менять по ИД заявки или по ИД юзера?\
    try:
        status= request.data['data']['status']
    except:
        return Response(status = r_status.HTTP_400_BAD_REQUEST)
    if not status in ['отменён', 'завершён']:
        return Response(status = r_status.HTTP_400_BAD_REQUEST)
    try:
        req = Request.objects.filter(id = id, status = 'в работе')[0]
    except:
       return  Response(status = r_status.HTTP_404_NOT_FOUND, data = 'no such id or the status does not match or the admin is not set')
    if status == 'завершён':
        operation_util(req)
    req.status = status
    req.admin= admin_id
    req.finish_date = datetime.datetime.now(tz=pytz.UTC)
    req.save()
    return Response(status = r_status.HTTP_200_OK, data ={'data': RequestSerializer(req).data})
  
'''