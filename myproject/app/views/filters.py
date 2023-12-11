import datetime
import pytz
from app.models import UserProfile
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

def StatusFilter(objects, request, user:UserProfile):
     try:
          status_list = request.query_params['status_list']
     except:
            status_list = []
     if (len(status_list) ==0):
          if (user.is_staff==False and user.is_superuser==False):
               return (objects.filter(user = user).exclude(status__in = ['удалён', 'введён']))
          else:
            return( objects.all().exclude(status__in= ['удалён','введён']))
     status_list =status_list.split('|')
     if user.is_staff==False and user.is_superuser==False:
         return (objects.filter( user = user, status__in = status_list) )
     return (objects.filter( status__in = status_list) )
    


def RequestFilter(objects, request, user):
    return DateFilter(StatusFilter(objects,request, user),request)