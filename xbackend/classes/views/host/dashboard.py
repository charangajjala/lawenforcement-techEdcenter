from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import *

from django.http import JsonResponse

from classes.services import HostDashboardServices

class HostCurrentClassesAPI(APIView):
  permission_classes = [IsAuthenticated]

  def get(self,request):
    user = request.user
    try:
      response,status = HostDashboardServices.currentClasses(user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)
class HostPastClassesAPI(APIView):
  permission_classes = [IsAuthenticated]

  def get(self,request):
    user = request.user
    try:
      response,status = HostDashboardServices.pastClasses(user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)