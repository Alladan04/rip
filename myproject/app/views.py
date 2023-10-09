from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import psycopg2
from datetime import date
from django.http import UnreadablePostError
from .serializers import OperationSerializer,UserSerializer, OperationRequestSerializer,RequestSerializer
from .models import Operation,User,OperationRequest,Request
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
'''
data ={ 'data':{'orders': [
    {'id':1, 'name':'Сложение','img':'https://pngimg.com/uploads/plus/plus_PNG31.png','text':'Сложе́ние — одна из основных бинарных математических операций двух аргументов, результатом которой является новое число, получаемое увеличением значения первого аргумента на значение второго аргумента.', 'type':'Арифметический','price':123.0},
    {'id':2, 'name':'Вычитание', 'img':'https://cdn.icon-icons.com/icons2/1144/PNG/512/subtractsign_80955.png', 'text':'Вычита́ние — одна из вспомогательных бинарных математических операций двух аргументов, результатом которой является новое число, получаемое уменьшением значения первого аргумента на значение второго аргумента. ', 'type':'Арифметический','price':123.0},
    {'id':3, 'name':'Умножение', 'img':'https://cdn-icons-png.flaticon.com/512/1/1659.png','text':'Умноже́ние — одна из основных математических операций над двумя аргументами, которые называются множителями или сомножителями. ','type':'Арифметический', 'price':10.0},
    {'id':4, 'name':'Деление', 'img':'https://cdn-icons-png.flaticon.com/512/660/660236.png', 'text':'some text','type':'Арифметический', 'price':5.0},
    {'id':5, 'name':'XOR', 'img':'https://static.thenounproject.com/png/711172-200.png','text':'sometext','type':'Логический', 'prcie':12.0}
    ]}}
'''
'''
заметки
создание заявки происходит внутри вью услуг, там делаем метод пост, через который можем 
добавить продукт в заявку или создать новую заявку, если ее не существует (активной) можно проверить в таблице м-м
м-м хранит только активные заявки, если что они удаляются оттуда физически
из самой таблицы заявок удаляем заявки только логически

у м-м нет своего пк, используем составной пк

при гет-запросе в заявки, надо получить данные из таблиц м-м и услуги (заджойнить наверно как-то)


'''

class OperationListView(APIView):

    def get(self, request):
        try:
            input_text = request.data['text']
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
     
    def get(self, request, id):
        order = Operation.objects.filter(id = id)[0]
        serializer = OperationSerializer(order)
        return Response({'data':serializer.data})
    
    def put(self, request,id):
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
        data = Operation.objects.filter()#filter(id = id)[0]
        serializer = OperationSerializer(data)
        redirect(reverse('basic_url'))
        return Response({'data':serializer.data})

class UserView(APIView):
     def get(self, request, id):
        user = User.objects.filter(id = id)[0]
        serializer = UserSerializer(user)
        return Response({'data':serializer.data})
     '''def post(self, request):
            serializer = UserSerializer(data= request.data['data'])
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response ({'data':serializer.data})'''

class RequestListView(APIView):
     def get(self, request):
          #список надо по ИД юзера получать? 
        requests = Request.objects.all()
        serialized_list = [RequestSerializer(request).data for request in requests]
        return Response(data= {'data':serialized_list})
     
class RequestView(APIView):
     def get (self, request,id):
          request = Request.objects.filter(id = id)
          