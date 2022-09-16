from django.forms import model_to_dict
from rest_framework import serializers
from classes.serializers.host.host import HostResponse

from meta.serializers import GetFieldData,ChoiceField
import datetime

from collections import OrderedDict

from hosts.models import Host,Location
from hosts.serializers import AdminHostResponse,AdminLocationResponse

#Response getting bunch of classes
class ClassesResponse(serializers.Serializer):
  id = serializers.IntegerField()
  course = GetFieldData(lambda obj:obj.course.title)
  instructor = GetFieldData(lambda obj:(obj.instructor.user.firstName+obj.instructor.user.lastName))
  startDate = serializers.DateField()
  endDate = serializers.DateField()
  
  def to_representation(self, instance):
      res = super().to_representation(instance)
      earlyFee = instance.earlyFee
      regularFee = instance.regularFee
      lateFee = instance.lateFee
      today = datetime.datetime.now()
      classStart = datetime.datetime.combine(instance.startDate,instance.startTime)
      difference = classStart - today
      if classStart > today:
        if difference.days >= 90:
          res['fee'] = earlyFee
        if 30<=difference.days<90:
          res['fee'] = regularFee
        if 0<=difference.days<30:
          res['fee'] = lateFee
      else:
        res['fee'] = lateFee
      if instance.host:
        res['host'] = instance.host.name
      if instance.location:
        res['location'] = instance.location.name
      data = OrderedDict([(key,res[key]) for key in res if res[key] is not None])
      return data


#Response After creating a class
class ClassResponse(serializers.Serializer):
  id = serializers.IntegerField()
  course = GetFieldData(lambda obj:obj.course.id)
  instructor = GetFieldData(lambda obj:obj.instructor.id)
  startDate = serializers.DateField()
  endDate = serializers.DateField()
  startTime = serializers.TimeField()
  endTime = serializers.TimeField()
  earlyFee = serializers.DecimalField(max_digits=19,decimal_places=2)
  regularFee = serializers.DecimalField(max_digits=19,decimal_places=2)
  lateFee = serializers.DecimalField(max_digits=19,decimal_places=2)
  def to_representation(self, instance):
      res = super().to_representation(instance)
      earlyFee = instance.earlyFee
      regularFee = instance.regularFee
      lateFee = instance.lateFee
      today = datetime.datetime.now()
      classStart = datetime.datetime.combine(instance.startDate,instance.startTime)
      difference = classStart - today
      print(difference.days)
      if difference.days >= 90:
        res['fee'] = earlyFee
      if 30<=difference.days<90:
        res['fee'] = regularFee
      if difference.days<30:
        res['fee'] = lateFee
      if instance.host:
        hostObj = Host.objects.get(id=instance.host.id)
        hostResponse = AdminHostResponse(hostObj)
        res['host'] = hostResponse.data
      if instance.location:
        locationObj = Location.objects.get(id=instance.location.id)
        locationResponse = AdminLocationResponse(locationObj)
        res['location'] = locationResponse.data
      data = OrderedDict([(key,res[key]) for key in res if res[key] is not None])
      return data

#Request and response of student verification
class ClassAttendeeVerificationRequest(serializers.Serializer):
  email = serializers.EmailField()

class ClassAttendeeVerificationResponse(serializers.Serializer):
  studentId = GetFieldData(lambda obj:obj.id)
  email = GetFieldData(lambda obj:obj.user.email)
  firstName = GetFieldData(lambda obj:obj.user.firstName)
  lastName = GetFieldData(lambda obj:obj.user.lastName)
  
  def to_representation(self, instance):
      res = super().to_representation(instance)
      rosterObj = self.context.get('rosterObj')
      if rosterObj:
        res['alreadyRegistered'] = True
      else:
        res['alreadyRegistered'] = False
      return res
