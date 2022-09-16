from rest_framework import serializers

from .applicant import *
from .admin_instructor import *
from meta.serializers import *

class DocRequest(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField(max_length=255)
  url = serializers.CharField(required=False)

  def validate_id(self,value):
    try:
        fileObj = File.objects.get(id=value)
        return value
    except File.DoesNotExist:
        raise serializers.ValidationError('Requested file was not uploaded try again')

class ApplicantListResponse(serializers.Serializer):
  id = serializers.IntegerField()
  firstName = serializers.SerializerMethodField()
  lastName = serializers.SerializerMethodField()
  email = serializers.SerializerMethodField()
  phone = serializers.SerializerMethodField()
  status = ChoiceField2(choices=Status.choices,write_only=True)
  
  def get_firstName(self,instance):
    return instance.user.firstName

  def get_lastName(self,instance):
    return instance.user.lastName

  def get_email(self,instance):
    return instance.user.email

  def get_phone(self,instance):
    return instance.user.phone

  

class ApplicantResponse(serializers.Serializer):
  id = serializers.IntegerField()
  userId = serializers.SerializerMethodField('get_userId')
  coursePreferences = CourseDetailRequest(many=True,allow_empty=True,required=False)
  docs = DocRequest(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=255)
  status = serializers.ChoiceField(choices=Status.choices,default=1)
  adminNotes = NoteRequest(many=True,allow_empty=True,required=False)

  def get_userId(self,instance):
        return instance.user.id

class ApplicantRequest(serializers.Serializer):
  userId = serializers.IntegerField()
  coursePreferences = CourseMethodRequest(many=True,allow_empty=True,required=False)
  docs = FileMethodRequest(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=255)
  status = ChoiceField(choices=Status.choices,write_only=True)
  adminNotes = NoteRequest(many=True,allow_empty=True,required=False)

  
