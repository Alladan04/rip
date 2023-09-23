from django.http import HttpResponse
from django.shortcuts import render


from datetime import date

data ={ 'data':{'orders': [
    {'id':1, 'title':'Сложение','img':'https://pngimg.com/uploads/plus/plus_PNG31.png','text':'some text', 'type':'Арифметический','price':123.0},
    {'id':2, 'title':'Вычитание', 'img':'https://cdn.icon-icons.com/icons2/1144/PNG/512/subtractsign_80955.png', 'text':'some text', 'type':'Арифметический','price':123.0},
    {'id':3, 'title':'Умножение', 'img':'https://cdn-icons-png.flaticon.com/512/1/1659.png','text':'some text','type':'Арифметический', 'price':10.0},
    {'id':4, 'title':'Деление', 'img':'https://cdn-icons-png.flaticon.com/512/660/660236.png', 'text':'some text','type':'Арифметический', 'price':5.0},
    {'id':5, 'title':'XOR', 'img':'https://static.thenounproject.com/png/711172-200.png','text':'sometext','type':'Логический', 'prcie':12.0}
    ]}}


def GetOrders(request):
    try:
        input_text = request.GET['text']
        #check = request.GET.getlist('check[]')
        if input_text:
            orders = [order for order in data['data']['orders'] if input_text.lower() in order['title'].lower()]
        return render(request, 'orders.html', {'data':{'orders':orders}})
    except:
        return render(request, 'orders.html', data)

    '''order = []     
    if check:
        for order_ in orders:
            if 'arifm' in check and order_['type'] =="Арифметический":
                order.append(order_)
            if  'logic' in check and order_['type'] == 'Логический':
                order.append(order_)'''
    

def GetOrder(request, id):
    order_ ={}
    for order in data['data']['orders']:
        if order['id'] == id:
            return render(request, 'order.html', order)
    
