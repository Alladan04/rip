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
from .conf import HOST, PORT
def get_us_id():
     return 1
def get_adm_id():
    return 2

class OperationListView(APIView):

    def get(self, request):
        try:
            input_text = request.query_params['text']
            if input_text:
                orders = Operation.objects.filter(status = "действует",name__icontains=input_text)
        except:
            orders = Operation.objects.filter(status = "действует")
        serialized = [OperationSerializer(order).data for order in orders]
        return Response({'data': serialized})
    
    def post(self, request):
            serializer = OperationSerializer(data= request.data['data'])
            serializer.is_valid(raise_exception=True)
            serializer.save()
            operations = Operation.objects.filter(status = "действует")
            serializer = [OperationSerializer(operation).data for operation in operations]
            return Response ({'data':serializer})
    
class OperationView(APIView):
    def post(self, request, id):#Добавление услуги в заявку?
        '''возвращает созданную/найденную заявку с полным списком услуг'''
        user_id =  get_us_id()
        try:
            
            req = Request.objects.get(user = User.objects.get(id = user_id), status='введён') 
            OperationRequest.objects.create(operation = Operation.objects.get(id = id), request = req, operand1 = request.data["data"]["operand1"], operand2 = request.data["data"]["operand2"])
            # сохранить новый оперэйшн-реквест в нашу бд   
            data = python_requests.get('http://'+HOST+PORT+'request/{id}'.format(id = req.id))
            return Response(status=200, data = data.json())
        except:
            try:
                req = Request.objects.create(user= User.objects.get(id = user_id), status = "введён",creation_date =datetime.datetime.now().astimezone())
                OperationRequest.objects.create(operation = Operation.objects.get(id = id), request = req,  operand1 = request.data["data"]["operand1"], operand2 = request.data["data"]["operand2"])
                #ЧТО ТУТ ВОЗВРАЩАТЬ И КАК ЭТО СДЕЛАТЬ????
                data = python_requests.get('http://'+HOST+PORT+'request/{id}'.format(id = req.id))
                return Response(status=200, data = data.json())
            except:
                return Response (status = 400, data = "Bad Request. Probably incorrect request body or the operation you are referring to does not exist")
     
    def get(self, request, id):
        order = Operation.objects.filter(id = id)[0]
        serializer = OperationSerializer(order)
        return Response({'data':serializer.data})
    
    def put(self, request,id):
            '''возвращяет измененную операцию'''
            operation = Operation.objects.filter(id=id)[0]
            serializer = OperationSerializer(operation, data = request.data['data'], partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data':serializer.data})
       
    def delete(self, request, id):
        #query = "UPDATE operations SET status = 'удален' WHERE id = {id_}".format(id_= id)#change this to ORM!!!
        operation = Operation.objects.get(id = id)
        operation.status = 'удален'
        operation.save()
        #data = Operation.objects.filter(id = id)[0]
        operations = Operation.objects.filter(status = "действует")
        serialized = [OperationSerializer(order).data for order in operations]
        #serializer = OperationSerializer(data)
        redirect(reverse('basic_url'))
        return Response({'data':serialized})
