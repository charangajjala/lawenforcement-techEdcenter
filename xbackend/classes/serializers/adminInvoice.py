from rest_framework import serializers
from instructors.serializers import ContactRequest
from users.serializers import AddressRequest,UserRequest
from meta.serializers import ChoiceField2,ChoiceField
from classes.models import Invoice,Class,Roster
from meta.serializers import GetFieldData

from collections import OrderedDict

class AttendeeRequest(serializers.Serializer):
  id = serializers.IntegerField()
  firstName = serializers.CharField()
  lastName = serializers.CharField()
  email=serializers.EmailField()

class AdminInvoiceRequest(serializers.Serializer):
  promoId=serializers.IntegerField(required=False)
  pmrAgency = serializers.CharField()
  pmrContact = ContactRequest()
  pmrAddress = AddressRequest()
  type = ChoiceField2(choices=Invoice.InvoiceType.choices)
  cls = serializers.IntegerField()
  paymentMethod = ChoiceField2(choices=Invoice.PayMethod.choices)
  paid=serializers.BooleanField(default=False)
  paidDate = serializers.DateField()
  refund = serializers.BooleanField()
  refundDate = serializers.DateField()
  refundNotes = serializers.CharField()
  price = serializers.DecimalField(max_digits=19,decimal_places=2,)
  totalPrice = serializers.DecimalField(max_digits=19,decimal_places=2)
  card = serializers.CharField()
  transactionId = serializers.CharField()
  purchaseOrder = serializers.CharField()
  checkNumber = serializers.CharField()
  eftAch = serializers.CharField()
  notes = serializers.CharField()
  attendees = AttendeeRequest(many=True)

class AdminInvoiceResponse(serializers.Serializer):
  pmrAgency = serializers.CharField()
  invoiceNum=serializers.IntegerField()
  pmrContact = ContactRequest()
  pmrAddress = AddressRequest()
  type = ChoiceField(choices=Invoice.InvoiceType.choices)
  paymentMethod = ChoiceField(choices=Invoice.PayMethod.choices)
  accessKey=serializers.CharField()
  created = serializers.DateTimeField()
  paid=serializers.BooleanField(default=False)
  paidDate = serializers.DateField()
  refund = serializers.BooleanField()
  refundDate = serializers.DateField()
  refundNotes = serializers.CharField()
  price = serializers.DecimalField(max_digits=19,decimal_places=2,)
  totalPrice = serializers.DecimalField(max_digits=19,decimal_places=2)
  card = serializers.CharField()
  transactionId = serializers.CharField()
  purchaseOrder = serializers.CharField()
  checkNumber = serializers.CharField()
  eftAch = serializers.CharField()
  notes = serializers.CharField()
  createdBy = UserRequest()

  def to_representation(self, instance):
    res = super().to_representation(instance)
    classObj = self.context.get('classObj')
    if classObj:
      res['cls']=classObj.id
      if classObj.inServiceInvoice:
        if classObj.inServiceInvoice.promo:
          res['promoId'] = classObj.inServiceInvoice.promo.id
    data = OrderedDict([(key,res[key]) for key in res if res[key] is not None])
    return data

class AdminInvoiceListResponse(serializers.Serializer):
  invoiceNum = serializers.IntegerField()
  pmrAgency = serializers.CharField()
  pmrContact = GetFieldData(lambda obj:obj.pmrContact.title)
  type = ChoiceField(choices=Invoice.InvoiceType.choices)
  paymentMethod = ChoiceField(choices=Invoice.PayMethod.choices)

  paid = serializers.BooleanField()
  refund = serializers.BooleanField()
  totalPrice = serializers.DecimalField(max_digits=10,decimal_places=2)
  created = serializers.DateTimeField()

  def to_representation(self, instance):
      res = super().to_representation(instance)
      invoiceObj = Invoice.objects.get(id=instance.id)
      try:
        classObj = Class.objects.get(inServiceInvoice=invoiceObj)
        res['class']=classObj.course.title
      except Class.DoesNotExist:
        rosterObj = Roster.objects.get(invoice=invoiceObj)
        res['class'] = rosterObj.cls.course.title
      finally:
        return res