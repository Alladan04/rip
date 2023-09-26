from django.contrib import admin

from . import models

admin.site.register(models.User)
admin.site.register(models.Operation)
admin.site.register(models.Request)
admin.site.register(models.OperationRequest)
