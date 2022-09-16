from rest_framework import serializers

from promos.models import Promo
from meta.serializers import ChoiceField,ChoiceField2

class AdminPromoRequest(serializers.Serializer):
  code = serializers.CharField()
  type = ChoiceField2(choices=Promo.Type.choices)
  value = serializers.CharField()
  singleUse = serializers.BooleanField(default=False)
  expiryDate = serializers.DateField()
  isActive = serializers.BooleanField(default=False)

class AdminPromoResponse(serializers.Serializer):
  id = serializers.IntegerField()
  code = serializers.CharField()
  type = ChoiceField(choices=Promo.Type.choices)
  value = serializers.CharField()
  singleUse = serializers.BooleanField()
  expiryDate = serializers.DateField()
  isActive = serializers.BooleanField()
  created = serializers.DateTimeField()