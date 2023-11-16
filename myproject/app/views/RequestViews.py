from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import psycopg2
from datetime import date
from django.http import UnreadablePostError
from ..serializers import OperationSerializer,UserSerializer, OperationRequestSerializer,RequestSerializer
from ..models import Operation,User,OperationRequest,Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
import datetime
from rest_framework.decorators import api_view
from  rest_framework.exceptions import bad_request
import requests as python_requests
import json
from rest_framework import status as r_status
from .filters import RequestFilter
import pytz
def get_us_id():
     return 1
def get_adm_id():
    return 2
class RequestListView(APIView):
    def get(self, request, format = None):
        '''по юзер_ид выдает список заявок, есть фильтрация по статусу заявки.
        фильтры устанавливаются в квери параметрах урла в виде
        status_list=статус1|статус2...и т.д.
        если передан статус, которого не существует, возвращает бэд реквест'''
        user_id = get_us_id()
        '''   try:
            status_list = request.query_params['status_list']
        except:
            status_list = []
        if (len(status_list) ==0):
            requests = Request.objects.filter(user_id=user_id)
        else:
            status_list =status_list.split('|')
            requests = Request.objects.filter(user_id = user_id, status__in = status_list) '''
        requests = RequestFilter(Request.objects,request, user_id)
        try:
            serialized_list = [RequestSerializer(request).data for request in requests]
            return Response(data= {'data':serialized_list})
        except:
            return Response( status = 400, data = "Bad Request")
   
class RequestView(APIView):
    def get (self, request,id):
        ''' возвращает заявку по ИД вместе со всеми услугами, которые в нее включены и их подробной информацией
        (возможно, это избыточно, и было бы достаточно вернуть элемент из м-м, ссылающийся на саму услугу по ключу)
        Если введен ИД несуществующей заявки, возвращает бэд реквест'''
        try:
            ob_request = Request.objects.filter(id = id)[0]
            opreqs= OperationRequest.objects.filter(request = ob_request)
            #operations = [opreq.operation for opreq in opreqs]
            #serialized_operations = [OperationSerializer(operation).data for operation in operations]
            serialized_opreq = [OperationRequestSerializer(opreq).data for opreq in opreqs]
            for i in serialized_opreq:
                i['operation'] = OperationSerializer(Operation.objects.get(id = i['operation'])).data
            serialized_request= RequestSerializer(ob_request).data
            return Response(data = {'data':{'request':serialized_request, 'items':serialized_opreq}})#'operations':serialized_operations}})
        except:
            return Response(status=400, data = "Bad Request. Probably the request you are referring to does not exist") 
    def delete(self,request,id):
        ''' меняет статус выбранной заявки текущего юзера на удалён
        потом удаляет все связанные элементы из м-м физически
        если подали ИД который не существует, возвращает бэд реквест'''
        try:
            user_id = get_us_id()
            ob_request = Request.objects.filter(id =id, user_id = user_id)[0]
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
        
@api_view(['Put'])
def form(request, id):
    user_id = get_us_id()
    #тут менять по ИД заявки или по ИД юзера?
    try:
        req = Request.objects.filter(id = id, user_id = user_id, status = 'введён')[0]
    except:
        return Response(status = r_status.HTTP_404_NOT_FOUND, data = 'no such id or the status does not match')
    req.status = 'в работе'
    req.form_date = datetime.datetime.now(tz=pytz.UTC)
    #req.finish_date = None
    req.save()
    return Response(status = r_status.HTTP_200_OK, data ={'data': RequestSerializer(req).data})

def operation_util( req: Request):
    item = OperationRequest.objects.filter(request = req)
    for i in item:
        a = i.operand1
        b = i.operand2
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
            

@api_view(['Put'])
def decline_accept(request, id):
    admin_id = get_adm_id()
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
    req.admin_id = admin_id
    req.finish_date = datetime.datetime.now(tz=pytz.UTC)
    req.save()
    return Response(status = r_status.HTTP_200_OK, data ={'data': RequestSerializer(req).data})
  
