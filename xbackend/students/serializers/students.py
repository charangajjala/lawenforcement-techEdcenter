from rest_framework import serializers
from .admin_students import *

class StandardStudentRequest(serializers.Serializer):
  userId = serializers.IntegerField()
  agencyName = serializers.CharField(max_length=255)
  docs = DocRequest(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=255)

class StandardStudentResponse(serializers.Serializer):
  userId = serializers.SerializerMethodField('get_userId')
  docs = DocResponse(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=255)
  agencyName = serializers.CharField(max_length=255)

  def get_userId(self,instance):
      return instance.user.id
