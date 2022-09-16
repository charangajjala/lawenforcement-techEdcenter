from rest_framework import serializers

from classes.models import Class,Location
from meta.serializers import GetFieldData,ChoiceField

class HostResponse(serializers.Serializer):
  id = serializers.IntegerField()
  course = GetFieldData(lambda obj:obj.course.title)
  instructor = GetFieldData(lambda obj:(obj.instructor.user.firstName+obj.instructor.user.lastName))
  startDate = GetFieldData(lambda obj:obj.startDate)
  endDate = GetFieldData(lambda obj:obj.endDate)
  location = GetFieldData(lambda obj:obj.location.name)
  type = ChoiceField(choices=Class.Type.choices)
  status = ChoiceField(choices=Class.Status.choices)
  invoiceNum = GetFieldData(lambda obj:obj.inServiceInvoice.invoiceNum)
  accessKey = GetFieldData(lambda obj:obj.inServiceInvoice.accessKey)
  paid = GetFieldData(lambda obj:obj.inServiceInvoice.paid)

  def to_representation(self, instance):
      res = super().to_representation(instance)
      locationId = instance.location.id
      locationObj = Location.objects.get(id=locationId)
      res['inServiceSeats'] = locationObj.seats
      return res