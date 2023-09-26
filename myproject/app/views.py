from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
import psycopg2
from datetime import date
from .models import Operation
'''
data ={ 'data':{'orders': [
    {'id':1, 'name':'Сложение','img':'https://pngimg.com/uploads/plus/plus_PNG31.png','text':'Сложе́ние — одна из основных бинарных математических операций двух аргументов, результатом которой является новое число, получаемое увеличением значения первого аргумента на значение второго аргумента.', 'type':'Арифметический','price':123.0},
    {'id':2, 'name':'Вычитание', 'img':'https://cdn.icon-icons.com/icons2/1144/PNG/512/subtractsign_80955.png', 'text':'Вычита́ние — одна из вспомогательных бинарных математических операций двух аргументов, результатом которой является новое число, получаемое уменьшением значения первого аргумента на значение второго аргумента. ', 'type':'Арифметический','price':123.0},
    {'id':3, 'name':'Умножение', 'img':'https://cdn-icons-png.flaticon.com/512/1/1659.png','text':'Умноже́ние — одна из основных математических операций над двумя аргументами, которые называются множителями или сомножителями. ','type':'Арифметический', 'price':10.0},
    {'id':4, 'name':'Деление', 'img':'https://cdn-icons-png.flaticon.com/512/660/660236.png', 'text':'some text','type':'Арифметический', 'price':5.0},
    {'id':5, 'name':'XOR', 'img':'https://static.thenounproject.com/png/711172-200.png','text':'sometext','type':'Логический', 'prcie':12.0}
    ]}}
'''
def get_orders_util():
    operations = Operation.objects.filter(status ="действует")
    data = {'data':{'orders':operations}}
    return data
def GetOrders(request):
    try:
        input_text = request.GET['text']
        operations = []
        if input_text:
            order = Operation.objects.filter(status = "действует",name__icontains=input_text)
            data = {'data':{'orders':order}}
        return render(request, 'orders.html', data )
    except:
        
        return render(request, 'orders.html',get_orders_util())

    

def GetOrder(request, id):
    order = Operation.objects.filter(id = id)[0]
    return render(request, 'order.html',{'name':order.name,  'type':order.type, 'text':order.description,'img':order.img_src})

def DeleteOrder (request, id):
    query = "UPDATE operations SET status = 'удален' WHERE id = {id_}".format(id_= id)
    conn = psycopg2.connect(dbname="rip", host="localhost", user="alla", password="1324", port="5432")
    cursor = conn.cursor()
    cursor.execute(query)
    conn.commit()   # реальное выполнение команд sql1
    cursor.close()
    conn.close()
    return redirect(reverse('basic_url'))