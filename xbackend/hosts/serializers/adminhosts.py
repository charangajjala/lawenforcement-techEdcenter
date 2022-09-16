from django.db.models.enums import Choices
from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from users.serializers import *
from instructors.serializers import *
from students.serializers import *
from courses.serializers import OperationRequest
from meta.serializers import *
from hosts.models import Host

from django.utils.translation import gettext as _
from meta.serializers import ChoiceField

class LocationRequest(serializers.Serializer):
  id = serializers.IntegerField()
  action = ChoiceField(choices=Action.choices,write_only=True)

class LocationResponse(serializers.Serializer):
  id=serializers.IntegerField()
  name = serializers.CharField()
  address = AddressRequest()

class DocResponse(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField()
  url = SerializerMethodField()

  def get_url(self,instance):
    id = instance.id
    image = File.objects.get(id=id)
    url = image.file.url
    return url

class AdminHostRequest(serializers.Serializer):
  isActive = serializers.BooleanField(default=False)
  name = serializers.CharField(max_length=255)
  address = AddressRequest()
  logo= serializers.IntegerField(required=isActive)
  website = serializers.CharField(required=isActive)
  contactUser = serializers.IntegerField()
  supervisorContact = ContactRequest(required=isActive)
  courses = CourseMethodRequest(many=True,allow_empty=True,required=False)
  hostingType = ChoiceField2(choices=Host.Type.choices)
  locations = OperationRequest(many=True,allow_empty=True,required=False)
  docs = FileRequest(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=255)
  adminNotes = serializers.ListField(
        child=serializers.CharField(max_length=511),
        allow_empty=True,
        required=False
    )
  status = ChoiceField2(choices=Host.Status.choices)

class AdminHostResponse(AdminHostRequest):
  id = serializers.IntegerField()
  courses =CourseDetailRequest(many=True,allow_empty=True,required=False)
  locations = LocationResponse(many=True,allow_empty=True,required=False)
  contactUser = serializers.SerializerMethodField('get_userid')
  docs = DocResponse(many=True,allow_empty=True,required=False)
  isDeleted = serializers.BooleanField()
  created = serializers.DateTimeField()
  adminNotes = NoteResponse(many=True,allow_empty=True,required=False)
  logo = serializers.SerializerMethodField('get_url')
  status = serializers.SerializerMethodField()
  hostingType = serializers.SerializerMethodField()

  def to_representation(self, instance):
    res = super().to_representation(instance)
    res['createdBy'] = dict(
        id = instance.createdBy.id,
        firstName = instance.createdBy.firstName,
        lastName = instance.createdBy.lastName
    ) if instance.createdBy else None
    res['history'] = [h.toDict() for h in instance.history.all()]
    return res

  def get_url(self,instance):
    fileobj = getattr(instance,'logo')
    id = getattr(fileobj,'id')
    file = File.objects.get(id=id)
    return file.name

  def get_userid(self,instance):
    return instance.contactUser.id

  #returns the value from the key
  def get_status(self,instance):
    return instance.get_status_display()
  
  def get_hostingType(self,instance):
    return instance.get_hostingType_display()

class HostsListResponse(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField(max_length=255)
  city = serializers.SerializerMethodField('get_city')
  state = serializers.SerializerMethodField('get_state')
  status = serializers.SerializerMethodField()
  isActive = serializers.BooleanField(default=False)
  created = serializers.DateTimeField()

  def get_city(self,instance):
    return instance.address.city

  def get_state(self,instance):
    return instance.address.state

  def get_status(self,instance):
    return instance.get_status_display()
