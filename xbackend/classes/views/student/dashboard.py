from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from django.http import JsonResponse

from classes.services import StudentClassServices,StudentTrackServices

class StudentCurrentClassesAPI(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request):
    user =request.user
    try:
      response,status = StudentClassServices.current(user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)

class StudentPastClassesAPI(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request):
    user =request.user
    try:
      response,status = StudentClassServices.past(user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)


class StudentTracksAPI(APIView):
  permission_classes = [IsAuthenticated]
  def get(self,request):
    user =request.user
    try:
      response,status = StudentTrackServices.getTracks(user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)

