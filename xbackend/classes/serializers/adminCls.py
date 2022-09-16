from django.forms.models import model_to_dict
from django.test.utils import require_jinja2
from rest_framework import serializers

from collections import OrderedDict

from meta.serializers import GetFieldData,ChoiceField,ChoiceField2
from classes.models import Class,Evaluation
from courses.serializers import OperationRequest
from students.serializers import NoteResponse
from classes.models import Roster
from courses.serializers import MaterialResponse
from classes.serializers.student import EvalutionResponse

class AdminClassRequest(serializers.Serializer):
  course = serializers.IntegerField()
  instructor = serializers.IntegerField()
  host = serializers.IntegerField(required=False)
  location = serializers.IntegerField(required=False)
  inServiceInvoice = serializers.IntegerField(required=False)

  # status = serializers.ChoiceField(choices = Class.Status.choices,write_only=True,default=1,required=False)
  # type = serializers.ChoiceField(choices = Class.Type.choices,write_only=True,default=1,required=False)
  status = ChoiceField2(choices=Class.Status.choices)
  type = ChoiceField2(choices=Class.Type.choices)
  deliveryType = ChoiceField2(choices = Class.DeliveryType.choices)

  startDate = serializers.DateField()
  endDate = serializers.DateField()
  startTime = serializers.TimeField()
  endTime = serializers.TimeField()

  earlyFee = serializers.DecimalField(max_digits=19,decimal_places=2)
  regularFee = serializers.DecimalField(max_digits=19,decimal_places=2)
  lateFee = serializers.DecimalField(max_digits=19,decimal_places=2)

  inServiceFee = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  inServiceSeats = serializers.IntegerField(required=False)
  onlineMeetingDetails = serializers.CharField(required=False)

  postedOnPTT = serializers.BooleanField(default=False)
  orderDate = serializers.DateField(required=False)
  orderDeliveryDate = serializers.DateField(required=False)
  orderTrackingNumber = serializers.CharField(required=False)
  orderCarrier = serializers.CharField(required=False)
  orderQuantity = serializers.IntegerField(max_value=100,min_value=0,required=False)
  orderPrice = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  orderNotes = serializers.CharField(required=False)
  flightPrice = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  flightInfo = serializers.CharField(required=False)
  carRentalPrice=serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  carRentalInfo = serializers.CharField(required=False)
  hotelPrice = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  hotelInfo = serializers.CharField(required=False)

  docs = OperationRequest(
    many = True,
    allow_empty = True,
    required=False,
  )
  adminDocs = OperationRequest(
    many = True,
    allow_empty = True,
    required=False,
  )  
  aar = serializers.ListField(
    child = serializers.CharField(),
    allow_empty = True,
    required=False
  )
  adminNotes = serializers.ListField(
      child=serializers.CharField(max_length=511),
      allow_empty=True,
      required=False
  )

class RosterResponse(serializers.Serializer):
  id = GetFieldData(lambda obj:obj.student.id)
  firstName = GetFieldData(lambda obj:obj.student.user.firstName)
  lastName = GetFieldData(lambda obj:obj.student.user.lastName)
  agency = GetFieldData(lambda obj:obj.cls.instructor.agencyName)
  email = GetFieldData(lambda obj:obj.student.user.email)
  phone = GetFieldData(lambda obj:obj.student.user.phone)
  invoiceNum = GetFieldData(lambda obj:obj.invoice.invoiceNum)
  attendance = serializers.BooleanField(default=False)

  def to_representation(self, instance):
    res = super().to_representation(instance)
    if instance.evaluation:
      res['evaluation'] = True
    else:
      res['evaluation'] = False
    return res


class AdminClassResponse(serializers.Serializer):
  id = serializers.IntegerField()
  course = GetFieldData(lambda obj:obj.course.id)
  instructor = GetFieldData(lambda obj:obj.instructor.id)
  status = ChoiceField(choices = Class.Status.choices,default=1)
  type = ChoiceField(choices = Class.Type.choices,default=1)
  deliveryType = ChoiceField(choices=Class.DeliveryType.choices)

  startDate = serializers.DateField()
  endDate = serializers.DateField()
  startTime = serializers.TimeField()
  endTime = serializers.TimeField()

  earlyFee = serializers.DecimalField(max_digits=19,decimal_places=2)
  regularFee = serializers.DecimalField(max_digits=19,decimal_places=2)
  lateFee = serializers.DecimalField(max_digits=19,decimal_places=2)

  inServiceFee = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  inServiceSeats = serializers.IntegerField(required=False)
  onlineMeetingDetails = serializers.CharField(required=False)

  postedOnPTT = serializers.BooleanField(default=False)
  orderDate = serializers.DateField(required=False)
  orderDeliveryDate = serializers.DateField(required=False)
  orderTrackingNumber = serializers.CharField(required=False)
  orderCarrier = serializers.CharField(required=False)
  orderQuantity = serializers.IntegerField(max_value=100,min_value=0,required=False)
  orderPrice = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  orderNotes = serializers.CharField(required=False)
  flightPrice = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  flightInfo = serializers.CharField(required=False)
  carRentalPrice=serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  carRentalInfo = serializers.CharField(required=False)
  hotelPrice = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  hotelInfo = serializers.CharField(required=False)

  adminNotes = NoteResponse(many=True,allow_empty=True)
  docs = MaterialResponse(many=True,allow_empty=True)
  adminDocs = MaterialResponse(many=True,allow_empty=True)  
  aar = serializers.ListField(
    child = serializers.CharField(),
    allow_empty = True,
    required=False
  )
  
  created = serializers.DateTimeField()

  def to_representation(self, instance):
      res = super().to_representation(instance)
      rosterObjs = Roster.objects.filter(cls=instance)
      rosterData = RosterResponse(rosterObjs,many=True)
      res['roster'] = rosterData.data
      evaluationList = []
      for roster in rosterObjs:
        if roster.evaluation:
          evaluationObj = Evaluation.objects.get(id=roster.evaluation.id)
          evaluationList.append(evaluationObj)
      evaluationData = EvalutionResponse(evaluationList,many=True)
      if len(evaluationList) != 0:
        res['evaluation'] = evaluationData.data
      if instance.host:
        res['host'] = instance.host.id
      if instance.location:
        res['location'] = instance.location.id
      if instance.inServiceInvoice:
        res['inServiceInvoice'] = instance.inServiceInvoice.invoiceNum
      data = OrderedDict([(key,res[key]) for key in res if res[key] is not None ])
      return data

class AdminClassesResponse(serializers.Serializer):
  id = serializers.IntegerField()
  course = GetFieldData(lambda obj:obj.course.title)
  instructor = GetFieldData(lambda obj:(obj.instructor.user.firstName+obj.instructor.user.lastName))
  students=serializers.SerializerMethodField()
  startDate = serializers.DateField()
  endDate = serializers.DateField()
  status = ChoiceField(choices=Class.Status.choices)
  type = ChoiceField(choices=Class.Type.choices)
  flight = serializers.BooleanField(default=False)
  car = serializers.BooleanField(default=False)
  hotel =serializers.BooleanField(default=False)
  material = serializers.BooleanField(default=False)

  def get_students(self,instance):
    classId = instance.id
    rosterObjs = Roster.objects.filter(cls=classId)
    return len(rosterObjs)

  def to_representation(self, instance):
      res = super().to_representation(instance)
      if instance.host:
        res['host'] = instance.host.name
      if instance.location:
        res['location'] = instance.location.name
      data = OrderedDict([(key,res[key]) for key in res if res[key] is not None])
      return data

class InserviceRosterRequest(serializers.Serializer):
  title = serializers.CharField(required=False)
  firstName =  serializers.CharField(max_length=255)
  lastName = serializers.CharField(max_length=255)
  email = serializers.EmailField()
  phone = serializers.CharField(max_length=20)
  agency = serializers.CharField(max_length=255)