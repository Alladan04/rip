from django.contrib import admin

from . import models
#from django.contrib.auth.models import User
admin.site.register(models.UserProfile)
admin.site.register(models.Operation)
admin.site.register(models.Request)
admin.site.register(models.OperationRequest)
