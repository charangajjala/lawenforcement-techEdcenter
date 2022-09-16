from django.db.models.query_utils import Q
from rest_framework import serializers

from instructors.serializers import ContactRequest
from users.serializers import AddressRequest
from meta.serializers import GetFieldData,ChoiceField2
from classes.models.invoice import Invoice
from classes.models import Class,Roster
from promos.models import Promo

class AttendeesRequest(serializers.Serializer):
  firstName = GetFieldData(lambda obj:obj.student.user.firstName)
  lastName = GetFieldData(lambda obj:obj.student.user.lastName)
  email=GetFieldData(lambda obj:obj.student.user.email)

class InvoiceResponse(serializers.Serializer):
  pmrAgency=serializers.CharField()
  pmrContact=ContactRequest()
  pmrAddress=AddressRequest()
  paymentMethod=ChoiceField2(choices=Invoice.PayMethod,write_only=True)
  paid=serializers.BooleanField(default=False)
  paidDate=serializers.DateField()
  price=serializers.DecimalField(max_digits=15,decimal_places=2)
  totalPrice=serializers.DecimalField(max_digits=15,decimal_places=2)
  card=serializers.CharField()
  transactionId=serializers.CharField()

  def to_representation(self, instance):
      res = super().to_representation(instance)
      #studentObj = Student.objects.get(id=self.context.get('studnetId'))
      rosterObjs = Roster.objects.filter(invoice=instance)
      # paid = 0
      # unpaid = 0
      # for rosterObj in rosterObjs:
      #   invoiceNum = rosterObj.invoice.invoiceNum
      #   invoiceObj = Invoice.objects.get(invoiceNum=invoiceNum)
      #   if invoiceObj.paid == True:
      #     paid+=paid
      #   else:
      #     unpaid+=unpaid
      # print(paid,unpaid,'\n\n')
      # res['total'] = unpaid*(int(classObj.inServiceInvoice.price))
      res['attendees'] = AttendeesRequest(rosterObjs,many=True).data
      cls = set()
      for roster in rosterObjs:
        cls.add(roster.cls)
      classObj = list(cls)[0]
      res['startDate'] = classObj.startDate
      res['endDate'] = classObj.endDate
      res['cls'] = classObj.course.title
      if instance.promo:
        promoObj = Promo.objects.get(id=instance.promo.id)
        res['code'] = promoObj.code
      return res

class InvoiceRequest(serializers.Serializer):
  totalPrice=serializers.DecimalField(max_digits=15,decimal_places=2)
  card = serializers.CharField(max_length=255)
  transactionID=serializers.CharField(max_length=255)