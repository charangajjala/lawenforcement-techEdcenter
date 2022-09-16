from django.db.models.query_utils import Q

from rest_framework.status import *

from classes.serializers import InvoiceResponse,InvoiceRequest
from classes.models import Invoice

class InvoiceServices:
  @classmethod
  def getInvoice(cls,invoiceNum,accessKey):
    try:
      invoiceObj = Invoice.objects.get(Q(invoiceNum=invoiceNum)&Q(accessKey=accessKey))
      invoiceResponse=InvoiceResponse(invoiceObj)
      response,status = invoiceResponse.data,HTTP_200_OK
    except Invoice.DoesNotExist:
      response,status = dict(error='Requested invoice is not found in the database'),HTTP_400_BAD_REQUEST
    except Invoice.MultipleObjectsReturned:
      response,status = dict(error='Two invoice cant have the same invoice Num and accessKey'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def postInvoice(cls,data,invoiceNum,accessKey,user):
    invoiceRequest = InvoiceRequest(data=data)
    try:
      if invoiceRequest.is_valid():
        validData = invoiceRequest.validated_data
        invoiceObj = Invoice.objects.get(Q(invoiceNum=invoiceNum)&Q(accessKey=accessKey))
        for k,v in validData:
          setattr(invoiceObj,k,v)
        setattr(invoiceObj,'createdBy',user)
        invoiceResponse = InvoiceResponse(invoiceObj)
        response,status = invoiceResponse.data,HTTP_200_OK        
    except Invoice.DoesNotExist:
      response,status = dict(error='Requested invoice is not found in the database'),HTTP_400_BAD_REQUEST
    except Invoice.MultipleObjectsReturned:
      response,status = dict(error='Two invoice cant have the same invoice Num and accessKey'),HTTP_400_BAD_REQUEST
    return response,status