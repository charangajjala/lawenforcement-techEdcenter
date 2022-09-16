from datetime import datetime
from importlib.metadata import requires
from rest_framework import serializers

from meta.serializers import GetFieldData,ChoiceField2
from instructors.serializers import ContactRequest
from users.serializers import AddressRequest
from classes.models.invoice import Invoice

class ClassRegistrationResponse(serializers.Serializer):
  invoiceNum = serializers.IntegerField()
  accessKey = serializers.CharField(max_length=50)
  url = serializers.CharField(max_length=255,required=False)

class ClassRegistrationRequest(serializers.Serializer):
  promoId = serializers.IntegerField(required=False)
  pmrAgency = serializers.CharField(max_length=255,)
  pmrContact = ContactRequest()
  pmrAddress = AddressRequest()
  paymentMethod = ChoiceField2(choices = Invoice.PayMethod.choices,write_only=True)
  type = ChoiceField2(choices=Invoice.InvoiceType.choices,write_only=True,default=1)
  paid = serializers.BooleanField(default=False)
  paidDate = serializers.DateField(default=None)
  price = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  totalPrice = serializers.DecimalField(max_digits=19,decimal_places=2,required=False)
  attendees = serializers.ListField(
    allow_empty= True,
    required = False,
  )