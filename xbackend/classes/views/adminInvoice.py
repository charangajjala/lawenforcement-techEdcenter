from typing import final
from typing_extensions import ParamSpec
from django.http import JsonResponse

from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import JSONParser

from classes.services import AdminInvoicesServices,AdminInvoiceSerivces

class AdminInvoicesAPI(APIView):
  permission_classes = [IsAdminUser,IsAuthenticated]

  def get(self,request):
    user = request.user
    try:
      response,status = AdminInvoicesServices.getInvoices(user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)

  def post(self,request):
    data=request.data
    user=request.user
    try:
      response,status = AdminInvoicesServices.createInvoice(data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

class AdminInvoiceAPI(APIView):
  permission_classes = [IsAdminUser,IsAuthenticated]

  def get(self,request,id):
    try:
      response,status = AdminInvoiceSerivces.getInvoice(id)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

  def put(self,request,id):
    data = request.data
    user=request.user
    try:
      response,status = AdminInvoiceSerivces.updateInvoice(id,data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

  def delete(self,request,id):
    user =request.user
    try:
      response,status = AdminInvoiceSerivces.deleteInvoice(id,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)