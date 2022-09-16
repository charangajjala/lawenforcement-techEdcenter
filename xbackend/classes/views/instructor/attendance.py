from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.status import *

from django.http import JsonResponse

from classes.services import AttendanceSerivices
from classes.models import Class

class AttendanceAPI(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request,id):
    code = request.data
    try:
      response,status = AttendanceSerivices.attendance(id,code)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

  def put(self,request,id):
    data = request.data
    try:
      response,status =AttendanceSerivices.updateAttendance(id,data)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)