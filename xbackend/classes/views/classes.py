
from django.http import JsonResponse

from rest_framework.views import APIView

from classes.services import *

class ClassesAPI(APIView):
  
  def get(self, request):
    params = request.query_params
    response,status = ClassService.getAll(params)
    return JsonResponse(response,safe=False,status=status)

class ClassAPI(APIView):
  
  def get(self,request,id):
    response,status = ClassService.getClass(id)
    return JsonResponse(response,status=status)

class ClassAttendeeVerificationAPI(APIView):

  def post(self,request,id):
    data = request.data
    try:
      response,status = AttendeeVerification.verfiy(data,id)   
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

class ClassRegisterAPI(APIView):

  def post(self,request,id):
    data = request.data
    try:
      response,status = ClassRegistrationService.register(id,data)
    except Exception as e:
      print(e)
      response,status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)