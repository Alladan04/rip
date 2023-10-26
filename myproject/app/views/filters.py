import datetime
import pytz
from datetime import datetime, timezone
def  OperationFilter(objects, request):
    if request.query_params.get('text'):
        return objects.filter(name__icontains=request.query_params.get('text'))
    return objects
    

def DateFilter(objects, request):
    lowerdate = "2020-01-01"
    higherdate = "2500-01-01"
    if request.query_params.get('downdate'):
        lowerdate = datetime.strptime(request.query_params.get('downdate'), '%Y-%m-%d|%H:%M:%S')
    if request.query_params.get('update'):
        higherdate = datetime.strptime(request.query_params.get('update'), '%Y-%m-%d|%H:%M:%S')
    return objects.filter(creation_date__gte = lowerdate, creation_date__lte = higherdate)

def StatusFilter(objects, request,user_id):
     try:
          status_list = request.query_params['status_list']
     except:
            status_list = []
     if (len(status_list) ==0):
          return( objects.filter(user_id=user_id).exclude(status = 'удалён'))
     status_list =status_list.split('|')
     return (objects.filter(user_id = user_id, status__in = status_list) )
    


def RequestFilter(objects, request,user_id):
    return DateFilter(StatusFilter(objects,request,user_id),request)