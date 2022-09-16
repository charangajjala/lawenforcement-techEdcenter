from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.status import *

from django.http import JsonResponse
from classes.services import StudentAttendanceServices,AdminStudentSignInServices

class StudentAttendanceAPI(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request,id):
    user = request.user
    attendanceCode = request.query_params.get('attendanceCode')
    try:
      response,status = StudentAttendanceServices.verify(id,user,attendanceCode)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

class AdminStudentSignInAPI(APIView):
  permission_classes = [IsAuthenticated,IsAdminUser]

  def post(self,request,id):
    data=request.data
    try:
      response,status = AdminStudentSignInServices.markPresent(id,data)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)