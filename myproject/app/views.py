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
import datetime
from rest_framework.decorators import api_view
from  rest_framework.exceptions import bad_request
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

статусы заявок: введен, сформирвоан/в обработке, принят/завершен, отколонен, удален
пользовательь может сформировать заявку (пут), удалить заявку(делит)
модератор может отклонить или принять

введен, когда добавляешь в корзину (такая только 1 или 0 заявок у каждого пользователя)
когда пользователь оформил заказ, заявка стала сформированной
потом она попадает к модератору и тот ставит статус принят или отклонен

статусы заявок: введён, удалён, в работе, завершён, отменён
статусы услуг: действует, удален
ВНИМАНИЕ!!! В моем варианте нужен собственный айди у м-м, так как могут быть несколько м-м, у которых 
одинаковые операция и заявка, но разные операнды. можно было бы в составной ключ включит еще и операнды,
конечно, но это кажется нецелесообразным
'''

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
        user_id =  get_us_id()
        try:
            req = Request.objects.get(user = User.objects.get(id = user_id), status='введён') 
            OperationRequest.objects.create(operation = Operation.objects.get(id = id), request = req, operand1 = request.data["data"]["operand1"], operand2 = request.data["data"]["operand2"])
            # сохранить новый оперэйшн-реквест в нашу бд   
            return Response(status=200)
        except:
            try:
                req = Request.objects.create(user= User.objects.get(id = user_id), status = "введён",creation_date =datetime.datetime.now().astimezone())
                OperationRequest.objects.create(operation = Operation.objects.get(id = id), request = req,  operand1 = request.data["data"]["operand1"], operand2 = request.data["data"]["operand2"])
                #Здесь надо создать новый реквест со статусом введен, и тоже создать новый м-м, сохранить его в бд м-м
                return Response(status=200)
            except:
                return Response (status = 404)
     
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
        #data = Operation.objects.filter(id = id)[0]
        operations = Operation.objects.filter(status = "действует")
        serialized = [OperationSerializer(order).data for order in operations]
        #serializer = OperationSerializer(data)
        redirect(reverse('basic_url'))
        return Response({'data':serialized})


class RequestListView(APIView):
    def get(self, request, format = None):
        '''по юзер_ид выдает список заявок, есть фильтрация по статусу заявки.
        фильтры устанавливаются в квери параметрах урла в виде
        status_list=статус1|статус2...и т.д.
        если передан статус, которого не существует, возвращает бэд реквест'''
        user_id = get_us_id()
        try:
            status_list = request.query_params['status_list']
        except:
            status_list = []
        if (len(status_list) ==0):
            requests = Request.objects.filter(user_id=user_id)
        else:
            status_list =status_list.split('|')
            requests = Request.objects.filter(user_id = user_id, status__in = status_list) 
        try:
            serialized_list = [RequestSerializer(request).data for request in requests]
            return Response(data= {'data':serialized_list})
        except:
            return Response( status = 400, data = "Bad Request")
     
@api_view(['Get'])
def get_request (request,id):
    try:
        request = Request.objects.filter(id = id)[0]
        opreqs= OperationRequest.objects.filter(request = request)
        #operations = [opreq.operation for opreq in opreqs]
        #serialized_operations = [OperationSerializer(operation).data for operation in operations]
        serialized_opreq = [OperationRequestSerializer(opreq).data for opreq in opreqs]
        for i in serialized_opreq:
            i['operation'] = OperationSerializer(Operation.objects.get(id = i['operation'])).data
        serialized_request= RequestSerializer(request).data
        return Response(data = {'data':{'request':serialized_request, 'items':serialized_opreq}})#'operations':serialized_operations}})
    except:
        return Response(status=400, data = "Bad Request. Probably the request you are referring to does not exist") 
