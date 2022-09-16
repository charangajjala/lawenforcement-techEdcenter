from rest_framework import serializers
from users.serializers import *
from hosts.models import Host
from hosts.serializers import LocationRequest,LocationResponse
from instructors.serializers import *
from . import *
from django.utils.translation import gettext as _
from meta.serializers import *

class StandardHostRequest(serializers.Serializer):
  name = serializers.CharField()
  address = AddressRequest()
  logo = serializers.IntegerField()
  website = serializers.URLField()
  contactUser = serializers.IntegerField()
  supervisorContact = ContactRequest()
  courses = CourseMethodRequest(many=True,allow_empty=True,required=False)
  hostingType = ChoiceField2(choices=Host.Type.choices,required=False)
  locations = LocationRequest(many=True,allow_empty=True,required=False)
  docs = FileRequest(many=True,allow_empty=True,required=False)
  comments = serializers.CharField(max_length=255)

class StandardHostResponse(StandardHostRequest):
  id=serializers.IntegerField()
  logo = serializers.URLField()
  locations = LocationResponse(many=True,allow_empty=True,required=False)
  courses = CourseDetailRequest(many=True,allow_empty=True,required=False)
  hostingType = ChoiceField(choices=Host.Type.choices,)
  contactUser = serializers.SerializerMethodField('get_userid')
  docs = DocResponse(many=True,allow_empty=True,required=False)

  def get_userid(self,instance):
    return instance.contactUser.id

class HostListResponse(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField()