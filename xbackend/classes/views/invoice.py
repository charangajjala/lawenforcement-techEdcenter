from django.http import JsonResponse
from rest_framework import permissions
from rest_framework.status import *

from rest_framework.views import APIView

from classes.services import InvoiceServices

class InvoiceAPI(APIView):


  def get(self,request):
    invoiceNum = request.query_params.get('invoiceNum')
    accessKey = request.query_params.get('accessKey')
    try:
      response,status = InvoiceServices.getInvoice(invoiceNum,accessKey)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)
    
  def post(self,request):
    data = request.data
    user = request.user
    invoiceNum = request.query_params.get('invoiceNum')
    accessKey = request.query_params.get('accessKey')
    try:
      response,status = InvoiceServices.postInvoice(data,invoiceNum,accessKey,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)
