from rest_framework import serializers
from .models import Hours
from meta.serializers import ChoiceField2

class HoursRequest(serializers.Serializer):
  date =serializers.DateField()
  hours = serializers.IntegerField()
  type = ChoiceField2(choices=Hours.Type.choices)

