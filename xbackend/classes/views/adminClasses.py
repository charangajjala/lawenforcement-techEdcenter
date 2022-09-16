from django.http import JsonResponse

from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import JSONParser

from classes.services import AdminClassServices

# Create your views here.
class AdminClassesAPI(APIView):

  permission_classes = [IsAuthenticated,IsAdminUser]
  parser_classes = [JSONParser]

  def post(self,request):
    data = request.data.copy()
    user = request.user
    try:
      response,status = AdminClassServices.createClass(data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

  def get(self,request):
    params = request.query_params
    response,status = AdminClassServices.getClasses(params)
    return JsonResponse(response,status=status,safe=False)

class AdminClassAPI(APIView):

  permission_classes = [IsAuthenticated,IsAdminUser]
  parser_classes = [JSONParser]

  def get(self,request,id):
    response,status = AdminClassServices.getClass(id)
    return JsonResponse(response,status=status)

  def put(self,request,id):
    data = request.data
    user = request.user
    try:
      response,status = AdminClassServices.updateClass(id,data,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

  def delete(self,request,id):
    user = request.user
    try:
      response,status  = AdminClassServices.deleteClass(id,user)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

class AdminInserviceServices(APIView):

  def post(self,request,id):
    data=request.data
    try:
      response,status  = AdminClassServices.addRoster(id,data)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)