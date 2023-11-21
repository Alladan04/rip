from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import psycopg2
from datetime import date
from django.http import UnreadablePostError
import pytz
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
import random
from rest_framework import status as r_status
from .conf import HOST, PORT,BUCKET, BASE_IMG
from ..minio.MinioClass import MinioClass
def get_us_id():
     return 1
def get_adm_id():
    return 2

def getImage(img_name:str):
    minio = MinioClass()
    #FineData = serializer.data
    #FineData.update({'image': minio.getImage('fines', serializer.data['fine_id'], serializer.data['picture'])})
    img = minio.getImage(buck_name=BUCKET, object_name=img_name)
    return img

def postImage(request:Request,img_name:str ):
    minio = MinioClass()
    minio.addImage(buck_name=BUCKET, image_base64=request.data['data']['image'], object_name=img_name)
 

def putImage(request:Request, img_name:str):
    minio = MinioClass()
    minio.removeImage(buck_name=BUCKET, object_name=img_name)
    minio.addImage(buck_name=BUCKET, image_base64=request.data['data']['image'], object_name=img_name)
   
class OperationListView(APIView):

    def get(self, request):
        user_id = get_us_id()
        try:
            input_text = request.query_params['text']
            if input_text:
                orders = Operation.objects.filter(status = "действует",name__icontains=input_text)
            else:
                orders = Operation.objects.filter(status = "действует")

        except:
            orders = Operation.objects.filter(status = "действует")
        serialized = [OperationSerializer(order).data for order in orders]
        for serialized_item in serialized:
            if serialized_item['img'] ==None:
                serialized_item['image']=getImage(BASE_IMG)
            else:
               serialized_item['image']= getImage(serialized_item['img'])
        req = Request.objects.filter (user_id = user_id, status = 'введён')
        if req:
             req_id = req[0].id
        else: 
            req_id = None
        return Response({'data': serialized, 'request_id':req_id})
    
    def post(self, request):#добавление услуги
            #тут если приложил картинку то обязательно нужно приложить и ее название с расширением
            #try:
                serializer = OperationSerializer(data= request.data['data'])
                
                keys = request.data['data'].keys()
                if ('image' in keys and 'img' in keys):
                    postImage(request, img_name = request.data['data']['img'])
                elif 'image' in keys:
                    img =f"img_{datetime.datetime.now()}.png"
                    postImage(request, img_name =img ) 
                    serializer.img = img
                serializer.is_valid(raise_exception=True)
                serializer.save()
            #TODO: save picture to minio and the picture name to database in operations.img field
            #if no imgae is attached then use the basic picture
            #if no name is attached then generate new name OR return an error (2-ND VARIANT MAY BE BETTER)
                return_data = python_requests.get('http://'+HOST+PORT+'operation/')
                return Response(status=200, data = return_data.json())
    '''except:
                return Response(status = r_status.HTTP_400_BAD_REQUEST)
            operations = Operation.objects.filter(status = "действует")
            serializer = [OperationSerializer(operation).data for operation in operations]
            return Response ({'data':serializer})'''
    
class OperationView(APIView):
    def post(self, request, id):#Добавление услуги в заявку?
        '''возвращает созданную/найденную заявку с полным списком услуг
        если один операнд в теле запроса, то второй автоматически =0
        если нет операндов в теле запроса или их названия переданы неправильно, то оба = 0
        если нет операции по введенному ИД, то 404
        есл нет поля data в теле запроса, то вернет 400 '''
        user_id =  get_us_id()
        ''' try:
            request_keys = request.data['data'].keys()
        except:
             return Response(status=r_status.HTTP_400_BAD_REQUEST, data = 'incorrect request body')
        if "operand1" in request_keys:
                op1 = request.data['data']['operand1']
        else:
                op1 = 0
        if "operand2" in request_keys:
                op2 = request.data['data']['operand2']
        else:
                op2 = 0
        '''
        try:
            
            req = Request.objects.filter(user = User.objects.get(id = user_id), status='введён')[0]
        except:
            req = Request.objects.create(user= User.objects.get(id = user_id), status = "введён",creation_date =datetime.datetime.now(tz=pytz.UTC))
        try:
            OperationRequest.objects.create(operation = Operation.objects.get(id = id), request = req)
        except:
             return Response(status=r_status.HTTP_404_NOT_FOUND, data = 'the operation you are referring to does not exist')
        # сохранить новый оперэйшн-реквест в нашу бд   '''
        data = python_requests.get('http://'+HOST+PORT+'request/{id}'.format(id = req.id))
        return Response(status=200, data = data.json())
    
       
     
    def get(self, request, id):
        order = Operation.objects.filter(id = id)[0]
        serializer = OperationSerializer(order)
        if serializer.data['img'] ==None:
                image=getImage(BASE_IMG)
        else:
               image= getImage(serializer.data['img'])
        serializer.data["image"] = image
        return Response({'data':serializer.data, "image":image})
    
    def put(self, request,id):
            '''возвращяет измененную операцию
            было бы классно добавить здесь ограничение на поля, которые можно менять
            например, статус этой функцией менять должно быть нельзя'''
            operation = Operation.objects.filter(id=id)[0]
            
            req_data_keys = request.data['data'].keys()
            if 'image' in req_data_keys and 'img' in req_data_keys:
                putImage(request=request, img_name = request.data['data']['img'])
            elif 'image' in req_data_keys:
                if operation.img:
                    putImage(request=request, img_name=operation.img)
                else:
                    img =f"img_{datetime.datetime.now()}.png"
                    putImage(request=request, img_name = img)
                    operation.img = img
            serializer = OperationSerializer(operation, data = request.data['data'], partial = True)
            serializer.is_valid(raise_exception=True)
            #TODO: save the image to minio if it is in the request (check boris)
            serializer.save()
            return_data = python_requests.get('http://'+HOST+PORT+'operation/{id_}/'.format (id_ = id))
            return Response(status=200, data = return_data.json())
       
    def delete(self, request, id):
        '''делает ТОЛЬКО логическое удаление операции из бд.
        картинка изз минио не удаляется тоже'''
        #query = "UPDATE operations SET status = 'удален' WHERE id = {id_}".format(id_= id)#change this to ORM!!!
        operation = Operation.objects.get(id = id)
        operation.status = 'удален'
        operation.save()
       # operations = Operation.objects.filter(status = "действует")
        #serialized = [OperationSerializer(order).data for order in operations]
        return_data = python_requests.get('http://'+HOST+PORT+'operation/')
        return Response(status=200, data = return_data.json())
       