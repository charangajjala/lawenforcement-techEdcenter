from rest_framework import serializers
from users.serializers import AddressRequest
from instructors.serializers import ContactRequest,NoteRequest  
from students.serializers import *

class AdminLocationRequest(serializers.Serializer):
  isActive = serializers.BooleanField(default=False)
  name = serializers.CharField(max_length=255)
  address = AddressRequest(required=isActive)
  seats = serializers.IntegerField(required=isActive)
  isWifiEnabled = serializers.BooleanField(default=False)
  isAudioEnabled = serializers.BooleanField(default=False)
  isProjectionEnabled = serializers.BooleanField(default=False)
  isMicEnabled = serializers.BooleanField(default=False)
  hasFlatScreens = serializers.BooleanField(default=False)
  locationContact = ContactRequest()
  closestAirports = serializers.CharField(default=None)
  intel = serializers.ListField(
        child=serializers.CharField(max_length=511),
        allow_empty=True,
        write_only=True,
        required=False
    )
  adminNotes = serializers.ListField(
        child=serializers.CharField(max_length=511),
        allow_empty=True,
        write_only=True,
        required=False
    )
  notes = serializers.CharField(default=None)

class AdminLocationResponse(AdminLocationRequest):
  id = serializers.IntegerField()
  isDeleted = serializers.BooleanField(default=False)
  created = serializers.DateTimeField()
  adminNotes = NoteResponse(many=True,allow_empty=True,required=False)

  def to_representation(self, instance):
    res = super().to_representation(instance)
    res['createdBy'] = dict(
        id = instance.createdBy.id,
        firstName = instance.createdBy.firstName,
        lastName = instance.createdBy.lastName
    ) if instance.createdBy else None
    res['history'] = [h.toDict() for h in instance.history.all()]
    return res

class AdminLocationsListResponse(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField(max_length=255)
  city = serializers.SerializerMethodField('get_city')
  state = serializers.SerializerMethodField('get_state')
  seats = serializers.IntegerField()
  isActive = serializers.BooleanField(default=False)
  created = serializers.DateTimeField()
  adminNotes = NoteResponse(many=True,allow_empty=True,required=False)

  def get_city(self,instance):
    return instance.address.city

  def get_state(self,instance):
    return instance.address.state
