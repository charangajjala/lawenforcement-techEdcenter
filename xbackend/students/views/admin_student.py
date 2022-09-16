from django.http.response import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import JSONParser

from students.services import *

class AdminStudentsAPI(APIView):

  permission_classes = [IsAuthenticated,IsAdminUser]
  parser_classes = [JSONParser]

  def post(self, request):
    """
      CREATE A STUDENT
    """
    currentUser = request.user
    data = request.data.copy()

    try:
      response,status = AdminStudentsServices.createStudent(currentUser,data)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response, status=status)
    

  def get(self,request):
    """
      GET A LIST OF INSTRUCTORS
    """
    params = request.query_params
    response,status = AdminStudentsServices.getAllStudents(params)
    return JsonResponse(response,safe=False,status=status)

    
class AdminStudentAPI(APIView):

  permission_classes = [IsAuthenticated,IsAdminUser]
  parser_classes = [JSONParser]

  def get(self,request, id):
    try:
      response,status = AdminStudentServices.getStudentProfile(id)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response, status=status)

  def put(self,request,id):
    currentUser = request.user
    data = request.data.copy()
    try:
      response,status = AdminStudentServices.updateStudentProfile(id,currentUser,data)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response, status=status)


  def delete(self,request,id):
    currentUser = request.user
    try:
      response,status = AdminStudentServices.deleteStudent(id,currentUser)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response, status=status)