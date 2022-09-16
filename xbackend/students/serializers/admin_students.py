from rest_framework import serializers
from django.db import models
from django.utils.translation import gettext as _
from meta.serializers import ChoiceField,GetFieldData

class Action(models.IntegerChoices):
    ADD = 1, _('ADD')
    REMOVE = 2, _('REMOVE')

class DocRequest(serializers.Serializer):
  id = serializers.IntegerField()
  action = ChoiceField(choices=Action.choices,default=1)

""" class NoteRequest(serializers.Serializer):
  text = serializers.CharField(max_length=511)
  created = serializers.CharField(max_length=255)
  createdBy = serializers.CharField(max_length=255) """

class StudentRequest(serializers.Serializer):
  isActive = serializers.BooleanField(default=False)
  userId = serializers.IntegerField()
  agencyName = serializers.CharField(max_length=255,required=isActive)
  docs = DocRequest(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=255,required=False)
  adminNotes = serializers.ListField(
        child=serializers.CharField(max_length=511),
        allow_empty=True,
        required=False
    )

class DocResponse(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField(max_length=255)
  url = serializers.CharField(max_length=255, read_only=True)

class NoteResponse(serializers.Serializer):
  text = serializers.CharField(max_length=255)
  created = serializers.DateTimeField()
  
  def to_representation(self, instance):
      res = super().to_representation(instance)
      res['createdBy'] = dict(
          id = instance.createdBy.id,
          firstName = instance.createdBy.firstName,
          lastName = instance.createdBy.lastName
      ) if instance.createdBy else None
      return res 

class StudentResponse(serializers.Serializer):
  id = serializers.IntegerField()
  agencyName = serializers.CharField(max_length=255)
  userId = serializers.SerializerMethodField('get_userId')
  docs = DocResponse(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=255)
  adminNotes = NoteResponse(many=True,allow_empty=True,required=False)
  isActive = serializers.BooleanField(default = False)
  isDeleted = serializers.BooleanField(default=False)
  created = serializers.DateTimeField()

  def get_userId(self,instance):
      return instance.user.id

  def to_representation(self, instance):
      res = super().to_representation(instance)
      res['createdBy'] = dict(
          id = instance.createdBy.id,
          firstName = instance.createdBy.firstName,
          lastName = instance.createdBy.lastName
      ) if instance.createdBy else None
      res['history'] = [h.toDict() for h in instance.history.all()]
      return res

class StudentsListResponse(serializers.Serializer):
  id = serializers.IntegerField()
  firstName = serializers.SerializerMethodField()
  lastName = serializers.SerializerMethodField()
  email = serializers.SerializerMethodField()
  phone = serializers.SerializerMethodField()
  agencyName = serializers.CharField(max_length=255)
  isActive = serializers.BooleanField(default=False)
  created = serializers.DateTimeField()

  def get_firstName(self,instance):
    return instance.user.firstName

  def get_lastName(self,instance):
    return instance.user.lastName

  def get_email(self,instance):
    return instance.user.email

  def get_phone(self,instance):
    return instance.user.phone