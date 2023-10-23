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
    def put(self, request, id): #change operands
        try:
            try:
               operation_r = OperationRequest.objects.filter(id=id,status = 'введён')[0]
            except:
               return Response(status = r_status.HTTP_404_NOT_FOUND)
            serializer = OperationRequestSerializer(operation_r, data = request.data['data'], partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({'data':serializer.data})
        except:
            return Response(status = 400, data = 'Bad request. Probably wrong request body or id')
