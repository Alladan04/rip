# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class OperationRequest(models.Model):
    operation = models.ForeignKey('Operation', models.DO_NOTHING, blank=True, null=True)
    request = models.ForeignKey('Request', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'operation_request'


class Operation(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    type = models.TextField(blank=True, null=True)  # This field type is a guess.
    price = models.FloatField(blank=True, null=True)  # This field type is a guess.
    description = models.TextField(blank=True, null=True)
    img_src = models.TextField(blank = True, null = True)

    class Meta:
        managed = False
        db_table = 'operations'


class Request(models.Model):
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.
    creation_date = models.DateField(blank=True, null=True)
    form_date = models.DateField(blank=True, null=True)
    finish_date = models.DateField(blank=True, null=True)
    admin = models.ForeignKey('User', models.DO_NOTHING, related_name='requests_admin_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'requests'


class User(models.Model):
    name = models.CharField(max_length=30, blank=True, null=True)
    password = models.CharField(max_length=30, blank=True, null=True)
    email = models.CharField(max_length=30, blank=True, null=True)
    is_admin = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users'
