from rest_framework import serializers
from meta.serializers import GetFieldData,ChoiceField,ChoiceField2
from .docs import DocsRequest
from ..student.evaluation import EvalutionResponse

from classes.models import Class,Roster

from collections import OrderedDict

class DocsResponse(serializers.Serializer):
  id = serializers.IntegerField()
  name = serializers.CharField()
  url = GetFieldData(lambda obj:obj.file.url)

class TravelInfoResponse(serializers.Serializer):
  rentalInfo = GetFieldData(lambda obj:obj.carRentalInfo)
  flightInfo = GetFieldData(lambda obj:obj.flightInfo)
  hotelInfo = GetFieldData(lambda obj:obj.hotelInfo)

class RosterResponse(serializers.Serializer):
  studentId = GetFieldData(lambda obj:Roster.objects.filter(cls = obj))

class CurrentClassesResponse(serializers.Serializer):
  id = serializers.IntegerField()
  course = GetFieldData(lambda obj:obj.course.title)
  startDate = serializers.DateField()
  startTime = serializers.TimeField()
  endDate = serializers.DateField()
  endTime = serializers.TimeField()
  host = GetFieldData(lambda obj:obj.host.name)
  location = GetFieldData(lambda obj:obj.location.name)
  status = ChoiceField(choices=Class.Status.choices)
  attendanceCode = serializers.IntegerField()
  docs = DocsResponse(many=True,allow_empty=True)

  def to_representation(self, instance):
      res = super().to_representation(instance)
      studentList = []
      travelInfo = TravelInfoResponse(instance)
      if travelInfo.data != None:
        res['travelInfo'] = travelInfo.data
      rosterObjs = Roster.objects.filter(cls=instance)
      res['bookedSeats'] = len(rosterObjs)
      res['totalSeats'] = instance.location.seats
      for roster in rosterObjs:
        rosterObj = dict(
          studentId = roster.student.id,
          title = roster.student.user.title,
          firstName = roster.student.user.firstName,
          lastName = roster.student.user.lastName,
          agency = roster.student.agencyName,
          attendance = roster.attendance
        )
        studentList.append(rosterObj)
      res['roster'] = studentList
      data = OrderedDict([(key,res[key]) for key in res if res[key] is not None])
      return data


class PastClassesResponse(serializers.Serializer):
  id = serializers.IntegerField()
  course = serializers.CharField()
  startDate = serializers.DateField()
  startTime = serializers.TimeField()
  endDate = serializers.DateField()
  endTime = serializers.TimeField()
  host = GetFieldData(lambda obj:obj.host.name)
  location = GetFieldData(lambda obj:obj.location.name)
  status = ChoiceField(choices=Class.Status.choices)
  # bookedSeats = GetFieldData(lambda obj:obj.location.seats)
  # totalSeats = GetFieldData(lambda obj:obj.location.seats)
  attendanceCode = serializers.IntegerField()
  docs = DocsResponse(many=True,allow_empty=True)
  aar = serializers.ListField(
    child=serializers.CharField(),
  )

  def to_representation(self, instance):
      res = super().to_representation(instance)
      studentList = []
      studentEvaluations = []
      travelInfo = TravelInfoResponse(instance)
      res['travelInfo'] = travelInfo.data
      rosterObjs = Roster.objects.filter(cls=instance)
      res['bookedSeats'] = len(rosterObjs)
      res['totalSeats'] = instance.location.seats
      for roster in rosterObjs:
        rosterObj = dict(
          studentId = roster.student.id,
          title = roster.student.user.title,
          firstName = roster.student.user.firstName,
          lastName = roster.student.user.lastName,
          agency = roster.student.agencyName,
          attendance = roster.attendance
        )
        evaluationObj = roster.evaluation
        if evaluationObj:
          studentEvaluations.append(evaluationObj)
        studentList.append(rosterObj)
      res['roster'] = studentList
      if evaluationObj:
        res['evaluation'] = EvalutionResponse(studentEvaluations,many=True).data
      data = OrderedDict([(key,res[key]) for key in res if res[key] is not None])
      return data


class CloseClassRequest(serializers.Serializer):
  aar = serializers.ListField(child=serializers.CharField(),allow_empty=True)
  attendance = serializers.ListField(child =serializers.IntegerField(),allow_empty=True)
  docs = DocsRequest(many=True,allow_empty=True,required=False)