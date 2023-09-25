from django.http import HttpResponse
from django.shortcuts import render


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

def GetOrders(request):
    operations = Operation.objects.all()
    data = {'data':{'orders':operations}}
    try:
        input_text = request.GET['text']
        #check = request.GET.getlist('check[]')
        if input_text:
            orders = [order for order in data['data']['orders'] if input_text.lower() in order.name.lower()]
        return render(request, 'orders.html', {'data':{'orders':orders}})
    except:
        return render(request, 'orders.html', data)

    

def GetOrder(request, id):
    operations = Operation.objects.all()
    data ={'data':{'orders':operations}}
    for order in data['data']['orders']:
        if order.id == id:
            return render(request, 'order.html', {'name':order.name, 'prcie':order.price, 'type':order.type, 'text':order.description,'img':order.img_src})
    
