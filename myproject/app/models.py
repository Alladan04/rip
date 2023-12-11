# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin,UserManager



class UserManager(UserManager):
     def create_user(self,username,password=None, **extra_fields):
        if not username:
            raise ValueError('User must have an email address')
        
        #username = username 
        user = self.model(username=username, **extra_fields) 
        user.set_password(password)
        user.save(using=self.db)
        return user

class UserProfile(AbstractBaseUser,PermissionsMixin):
    name = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=500, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True, unique = True)
    is_staff = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default = False)
    username = models.CharField(max_length=30, blank = True, null = True, unique = True)
    USERNAME_FIELD = 'username'
    objects =  UserManager()
    def __str__(self):
            return f"{self.username} | {self.id}" or ''
    
   


class Operation(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, blank=True, null=True)
    status = models.CharField(max_length =30, blank=True, null=True)  # This field type is a guess.
    type = models.CharField(max_length = 30, blank=True, null=True)  # This field type is a guess.
    price = models.FloatField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)
    img=models.CharField(max_length=30, blank = True, null = True) #models.ImageField(upload_to='uploads/')   

    class Meta:
        managed = True
        db_table = 'operations'


class Request(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True)##new field 20/10
    user = models.ForeignKey('UserProfile', models.DO_NOTHING, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_date = models.DateTimeField(blank=True, null=True)
    form_date = models.DateTimeField(blank=True, null=True)
    finish_date = models.DateTimeField(blank=True, null=True)
    admin = models.ForeignKey('UserProfile', models.DO_NOTHING, related_name='requests_admin_set', blank=True, null=True)
    def __str__(self):
            return f"Request #{self.id}" or ''
    class Meta:
        managed = True
        db_table = 'requests'
        


class OperationRequest(models.Model):
    operation = models.ForeignKey('Operation', models.DO_NOTHING, blank=True, null=True)
    request = models.ForeignKey('Request', models.DO_NOTHING, blank=True, null=True)
    operand1 = models.IntegerField(blank=True,null = True)
    operand2 = models.IntegerField(blank=True, null = True)
    result = models.IntegerField(blank = True, null = True)

    class Meta:
        managed=True
        db_table = 'operation_request'
