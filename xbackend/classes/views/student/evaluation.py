from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from classes.services import AdminStudentEvaluationSevices,StudentEvaluationServices

from django.http import JsonResponse

class AdminStudentEvaluationAPI(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request,id):
    data=request.data
    try:
      response,status = AdminStudentEvaluationSevices.sendEvaluation(id,data)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

class StudentEvaluationAPI(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request,id):
    data=request.data
    user = request.user
    try:
      response,status = StudentEvaluationServices.evaluation(id,data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)