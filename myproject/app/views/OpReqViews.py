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
from rest_framework import authentication, permissions
import datetime
from rest_framework.decorators import api_view
from  rest_framework.exceptions import bad_request
import requests as python_requests
import json
from rest_framework import status as r_status
from drf_yasg.utils import swagger_auto_schema
class OperationRequestView(APIView):
    def delete(self, request, id):
        #ТУТ наверно стоит вернуть гет из Реквест по реквест_ид из м-м
        #Но как это сделать?(
        try:
            op_req = OperationRequest.objects.get(id = id)
            if (op_req):
                req = op_req.request
                op = op_req.operation
                op_req.delete()
                return Response(status = r_status.HTTP_200_OK, data ='Deleted operation #{op} from request#{req}'.format(req = req, op=op))
        except:
            return Response(status = 400, data = 'Bad request. Probably the id you are referring to does not exist')
        return Response (status = 400, data = 'lol')
    @swagger_auto_schema(request_body=OperationRequestSerializer)
    def put(self, request, id): #change operands
        '''если подать ИД заявки, которая уже в работе/удалена/завершена/отменена, то вернет 400
        если подать невалидное тело запроса, вернет 400, 
        если подать ИД м-м, который не существует,то вернет 400
        иначе изменит операнд и вернет новое значение м-м'''
        try:
            try:
               operation_r = OperationRequest.objects.filter(id=id)[0]
            except:
               return Response(status = r_status.HTTP_404_NOT_FOUND)
            if operation_r.request.status =='введён':
                serializer = OperationRequestSerializer(operation_r, data = request.data['data'], partial = True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'data':serializer.data})
            else:
                return Response(status = r_status.HTTP_400_BAD_REQUEST, data = "Probably the request you are referring to is in the wrong status")
        except:
            return Response(status = 400, data = 'Bad request. Probably wrong request body or id')
