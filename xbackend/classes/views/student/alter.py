from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from django.http import JsonResponse

from classes.services import StudentAlterServices

class MoveStudentAPI(APIView):
  permission_classes=[IsAuthenticated]

  def post(self,request,id):
    data = request.data
    user=request.user
    try:
      response,status = StudentAlterServices.move(id,data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

class SubstituteStudentAPI(APIView):
  permission_classes=[IsAuthenticated]

  def post(self,request,id):
    data = request.data
    user=request.user
    try:
      response,status = StudentAlterServices.substitute(id,data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

class RemoveStudentAPI(APIView):
  permission_classes=[IsAuthenticated]

  def post(self,request,id):
    data = request.data
    user=request.user
    try:
      response,status = StudentAlterServices.remove(id,data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)