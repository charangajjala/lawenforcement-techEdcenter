from django.shortcuts import render
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.status import *

from .services import AdminHoursServices

# Create your views here.
class AdminHoursAPI(APIView):
  permission_classes=[IsAuthenticated,IsAdminUser]

  def get(self,request):
    query_params = request.query_params
    try:
      response,status = AdminHoursServices.get(query_params)
    except Exception as e:
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)


  def put(self,request):
    data=request.data
    user=request.user
    try:
      response,status = AdminHoursServices.update(data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

  def post(self,request):
    data=request.data
    user=request.user
    try:
      response,status = AdminHoursServices.create(data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)