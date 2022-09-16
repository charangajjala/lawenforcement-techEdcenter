from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.status import *

from django.http import JsonResponse

from classes.services import InstructorDocServices,CourseDocServices
class InstructorDocsAPI(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [MultiPartParser,JSONParser]

  def post(self,request,id):
    data = request.data
    try:
      response,status = InstructorDocServices.uploadDocs(id,data)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

class CourseDocsAPI(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [MultiPartParser,JSONParser]

  def get(self,request):
    user = request.user
    courseId = request.query_params
    try:
      response,status = CourseDocServices.getCourseDocs(user,courseId)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)

  def post(self,request):
    data =request.data
    courseId = request.query_params.get('courseId')
    try:
      response,status = CourseDocServices.uploadCoursedocs(data,courseId)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)