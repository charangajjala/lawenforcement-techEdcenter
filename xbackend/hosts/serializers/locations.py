from rest_framework import serializers

from instructors.serializers import AddressRequest,ContactRequest

class LocationRequest(serializers.Serializer):
  name = serializers.CharField(max_length=255)
  address = AddressRequest()
  seats = serializers.IntegerField()
  isWifiEnabled = serializers.BooleanField(default=False)
  isAudioEnabled = serializers.BooleanField(default=False)
  isProjectionEnabled = serializers.BooleanField(default=False)
  isMicEnabled = serializers.BooleanField(default=False)
  hasFlatScreens = serializers.BooleanField(default=False)  
  locationContact = ContactRequest()
  closestAirports = serializers.CharField(max_length=255)
  notes = serializers.CharField(max_length=255)
  adminNotes = serializers.ListField(
        child=serializers.CharField(max_length=511),
        allow_empty=True,
        required=False
    )
  intel = serializers.ListField(
        child=serializers.CharField(max_length=511),
        allow_empty=True,
        required=False
    )

class LocationResponse(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField(max_length=255)
  address = AddressRequest()
  seats = serializers.IntegerField()
  isWifiEnabled = serializers.BooleanField(default=False)
  isAudioEnabled = serializers.BooleanField(default=False)
  isProjectionEnabled = serializers.BooleanField(default=False)
  isMicEnabled = serializers.BooleanField(default=False)
  hasFlatScreens = serializers.BooleanField(default=False)
  locationContact = ContactRequest()
  closestAirports = serializers.CharField(max_length=255)
  notes = serializers.CharField(max_length=255)