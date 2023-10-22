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
from app import views
from django.urls import include, path
from rest_framework import routers
router = routers.DefaultRouter()
#router.register(r'', views.OperationView, basename='operations')
'''делать урл с пустым ИД нельзя, только если сделать ИД=0 и при этом значении выдавать список
но я не хочу костыльно делать, поэтому лучше сделаю, мб немного избыточно, но зато последовательно и понятно'''
urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path(r'order/<int:id>/', views.OperationView.as_view() , name='order_url'),
    path(r'order/', views.OperationListView.as_view(), name = 'order_list_url'),
    path(r'request/', views.RequestListView.as_view(), name = 'request_list_url'),
    path (r'request/<int:id>/', views.get_request, name = 'request_url')
]
