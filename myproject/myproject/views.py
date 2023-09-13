from django.http import HttpResponse
from django.shortcuts import render


from datetime import date

data ={ 'data':{'orders': [
    {'id':1, 'title':'Сложение','img':'https://pngimg.com/uploads/plus/plus_PNG31.png','text':'some text', 'type':'Арифметический'},
    {'id':2, 'title':'Вычитание', 'img':'https://png.pngtree.com/png-vector/20190223/ourlarge/pngtree-minus-vector-icon-png-image_696413.jpg', 'text':'some text', 'type':'Арифметический'},
    {'id':3, 'title':'Умножение', 'img':'https://cdn-icons-png.flaticon.com/512/1/1659.png','text':'some text','type':'Арифметический'},
    {'id':4, 'title':'Деление', 'img':'https://cdn-icons-png.flaticon.com/512/660/660236.png', 'text':'some text','type':'Арифметический'},
    {'id':5, 'title':'XOR', 'img':'https://static.thenounproject.com/png/711172-200.png','text':'sometext','type':'Логический'}
    ]}}


def GetOrders(request):
    return render(request, 'orders.html', data)

def GetOrder(request, id):
    order_ ={}
    for order in data['data']['orders']:
        if order['id'] == id:
            return render(request, 'order.html', order)
    
        
def sendText(request):
    input_text = request.POST['text']
    orders = {'data':{'orders':[order for order in data['data']['orders'] if input_text.lower() in order['title'].lower()]}}
    return render(request,'orders.html', orders )

def Filter(request):
    input_stuff = request.POST.getlist('check[]')
    order = []
    for order_ in data['data']['orders']:
        if 'arifm' in input_stuff and order_['type'] =="Арифметический":
            order.append(order_)
        if  'logic' in input_stuff and order_['type'] == 'Логический':
            order.append(order_)
    orders = {'data':{'orders':order}}
    return render(request,'orders.html', orders)