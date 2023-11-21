"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
#from app import views
from app.views import OperationViews, RequestViews, OpReqViews
from django.urls import include, path
from rest_framework import routers
router = routers.DefaultRouter()
#router.register(r'', views.OperationView, basename='operations')
'''делать урл с пустым ИД нельзя, только если сделать ИД=0 и при этом значении выдавать список
но я не хочу костыльно делать, поэтому лучше сделаю, мб немного избыточно, но зато последовательно и понятно'''
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path(r'operation/<int:id>/', OperationViews.OperationView.as_view() , name='operation_url'),
    path(r'operation/', OperationViews.OperationListView.as_view(), name = 'operation_list_url'),
    path(r'request/', RequestViews.RequestListView.as_view(), name = 'request_list_url'),
    path (r'request/<int:id>/', RequestViews.RequestView.as_view(), name = 'request_url'),
    path(r'request/form/<int:id>/', RequestViews.form, name = 'form_request_url'),
    path(r'request/finish/<int:id>/', RequestViews.decline_accept, name = 'finish_url'),
    path(r'request/operation/<int:id>/', OpReqViews.OperationRequestView.as_view(), name = 'operation_request_url'),

]
