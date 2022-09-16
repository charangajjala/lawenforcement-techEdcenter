from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from django.http import JsonResponse

from classes.services import InstructorDashboardServices

class InstructorCurrentClassesAPI(APIView):
  permission_classes = [IsAuthenticated]

  def get(self,request):
    user = request.user
    try:
      response,status = InstructorDashboardServices.currentClasses(user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)
class InstructorPastClassesAPI(APIView):
  permission_classes = [IsAuthenticated]

  def get(self,request):
    user = request.user
    try:
      response,status = InstructorDashboardServices.pastClasses(user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)

class CloseClassAPI(APIView):
  permission_classes = [IsAuthenticated]

  def post(self,request,id):
    data = request.data
    try:
      response,status = InstructorDashboardServices.closeClass(id,data)
    except Exception as e:
      print(e)
      response,status =e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)
