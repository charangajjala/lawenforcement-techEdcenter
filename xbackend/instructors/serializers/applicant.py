from django.db import models
from django.utils.translation import gettext as _

from rest_framework import serializers

from .admin_instructor import *
from users.serializers import * 
from meta.serializers import GetFieldData

class Status(models.IntegerChoices):
    RECEIVED = 1, _('Received')
    REVIEW = 2, _('In-Review')
    DEFER  = 3, _('Deferred')
    SHORTLIST = 4, _('Shortlisted')
    REJECT = 5, _('Rejected')
    ONBOARDING = 6, _('Shortlisted')
    HIRED = 7, _('Accepted')

class Action(models.IntegerChoices):
    ADD = 1, _('ADD')
    REMOVE = 2, _('REMOVE')

class CourseMethodRequest(serializers.Serializer):
  id = serializers.IntegerField()
  action = ChoiceField(choices=Action.choices,write_only=True)

class CourseDetailRequest(serializers.Serializer):
  id = serializers.IntegerField()
  title = serializers.SerializerMethodField()

  def get_title(self,instance):
    return instance.title


class FileMethodRequest(serializers.Serializer):
  id = serializers.IntegerField()
  action = ChoiceField(choices=Action.choices,write_only=True)

class DocRequest(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField(max_length=255)
  url = serializers.CharField(required=False)

class ApplicantRequest(serializers.Serializer):
  userId = serializers.IntegerField()
  courses = CourseMethodRequest(many=True,allow_empty=True,required=False)
  docs = FileMethodRequest(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=511)

class ApplicatUpdationRequest(serializers.Serializer):
  userId = serializers.SerializerMethodField()
  courses = CourseDetailRequest(many=True,allow_empty=True,required=False)
  docs = FileMethodRequest(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=511)

class ApplicatUpdationResponse(ApplicatUpdationRequest):
  id = serializers.IntegerField()
  courses = CourseDetailRequest(many=True,allow_empty=True,required=False)
  docs = DocRequest(many=True,allow_empty=True,required=False)