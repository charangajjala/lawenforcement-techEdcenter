from django.http.response import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

from students.services import *

class StandardStudentsAPI(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser]

  def post(self, request):
    data = request.data
    try:
      response,status = StandardStudentServices.createStudent(data)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response, status=status)

  def get(self,request):
    user = request.user
    try:
      response,status = StandardStudentServices.getProfile(user)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response, status=status)

  def put(self,request):
    data = request.data
    user = request.user
    try:
      response,status = StandardStudentServices.updateProfile(data,user)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response, status=status,safe=False)

class StudentDetailsAPI(APIView):
  def get(self,request,id):
    try:
      response,status = StandardStudentServices.getStudent(id)
    except Exception as e:
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)
