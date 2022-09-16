from django.http.response import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import JSONParser

from hosts.services import *

class AdminHostsAPI(APIView):

  permission_classes = [IsAuthenticated,IsAdminUser]
  parser_classes = [JSONParser]

  def post(self, request):
    currentUser = request.user
    data = request.data.copy()
    try:
      response,status = AdminHostsServices.createHost(data,currentUser)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response,safe=False, status=status)      

  def get(self,request):
    params = request.query_params
    try:
      response,status = AdminHostsServices.getAllHosts(params)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response,safe=False, status=status)      


class AdminHostAPI(APIView):

  permission_classes = [IsAuthenticated,IsAdminUser]
  parser_classes = [JSONParser]

  def get(self,request,id):
    try:
      response,status = AdminHostServices.getHost(id)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response,safe=False, status=status)      
  
  def put(self,request,id):
    currentUser = request.user
    data = request.data.copy()
    try:
      response,status = AdminHostServices.updateHost(id,data,currentUser)
      
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response,safe=False, status=status)

  def delete(self,request,id):
    currentUser = request.user
    try:
      response,status = AdminHostServices.deleteHost(id,currentUser)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response,safe=False, status=status)