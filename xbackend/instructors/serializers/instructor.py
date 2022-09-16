from rest_framework import serializers

from .admin_instructor import *
from users.serializers import AddressRequest
from meta.serializers import GetFieldData
from courses.serializers import MaterialResponse

class InstructorProfile(serializers.Serializer):
  image= GetFieldData(lambda obj:obj.image.file.url)
  dob = serializers.DateField()
  ssn = serializers.CharField(max_length=255)
  bio = serializers.CharField()
  firstName=GetFieldData(lambda obj:obj.user.firstName)
  lastName = GetFieldData(lambda obj:obj.user.lastName)
  agencyName = serializers.CharField(max_length=255)
  agencyAddress = AddressRequest()
  agencyContact = ContactRequest()
  emergencyContact = ContactRequest()
  docs =MaterialResponse(many=True,allow_empty=True,required=False)
  adminNotes = NoteRequest(many=True,allow_empty=True,required=False)
  isActive = serializers.BooleanField(default=False)
  retiredDate =serializers.DateField()
  closestAirports = serializers.CharField()
  preferredAirports = serializers.CharField()
  travelNotes = serializers.CharField()

class InstructorlistResponse(serializers.Serializer):
  id = serializers.IntegerField()
  image = serializers.SerializerMethodField()
  bio =serializers.CharField()
  firstName = serializers.SerializerMethodField()
  lastName = serializers.SerializerMethodField()

  def get_image(self,instance):
    return instance.image.file.url

  def get_firstName(self,instance):
    return instance.user.firstName

  def get_lastName(self,instance):
    return instance.user.lastName
