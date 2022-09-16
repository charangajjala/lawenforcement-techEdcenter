from rest_framework import serializers
from meta.serializers import ChoiceField2
from promos.models import Promo

class PromoResponse(serializers.Serializer):
  id = serializers.IntegerField()
  code = serializers.CharField()
  type = ChoiceField2(choices = Promo.Type.choices)
  value = serializers.CharField()