from os import stat
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from django.http.response import JsonResponse

from instructors.serializers import *
from instructors.services import *

class InstructorAPI(APIView):

  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser]

  def get(self,request):
    """
      GET INSTRUCTOR PROFILE
    """
    user = request.user
    try:
      response,status = InstructorService.getInstructorProfile(user)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return JsonResponse(response,safe=False, status=status) 

  def put(self,request):
    """
      UPDATE INSTRUCTOR PROFILE
    """
    user = request.user
    data = request.data.copy()
    try:
        response, status = InstructorService.updateProfile(user, data)
        print(response, status)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return JsonResponse(response, status=status)

class InstructorListAPI(APIView):

  def get(self,request):
    try:
      response,status = InstructorService.getInstructorList()
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return JsonResponse(response, status=status,safe=False)

class InstructorDetails(APIView):
  
  def get(self,request,id):
    try:
      response,status = InstructorService.getInstructor(id)
    except Exception as e:
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)