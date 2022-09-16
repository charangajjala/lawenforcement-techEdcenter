from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

from django.http import JsonResponse

from hosts.services import *

class StandardHostAPI(APIView):

  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser]

  def get(self,request):
    user = request.user
    try:
      response,status = StandardHostServices.hostProfile(user)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return JsonResponse(response,safe=False, status=status)

  def put(self,request):
    data = request.data
    currentUser = request.user
    try:
      response,status = StandardHostServices.updateProfile(data,currentUser)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return JsonResponse(response, status=status)

  def post(self,request):
    user = request.user
    data = request.data
    try:
      response,status = StandardHostServices.createHost(user,data)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response, status=status)

class AdditionalHostServices(APIView):
  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser]
  def get(self,request,id):
    try:
      response,status = StandardHostServices.getprofile(id)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response, status=status)

class HostListAPI(APIView):

  def get(self,request):
    try:
      response,status = StandardHostServices.getList()
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,safe=False,status=status)