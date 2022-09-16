from django.http.response import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from rest_framework.parsers import JSONParser
from rest_framework.status import *

from hosts.services import *

class AdminLocationsAPI(APIView):

  permission_classes = [IsAuthenticated,IsAdminUser]
  parser_classes = [JSONParser]

  def post(self,request):
    data = request.data
    currentUser = request.user
    try:
      response,status = AdminLocationsSerivices.createLocation(data,currentUser)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response, status=status)

  def get(self,request):
    params = request.query_params
    try:
      response,status = AdminLocationsSerivices.getAllLocations(params)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response,safe=False, status=status)

class AdminLocationAPI(APIView):

  permission_classes = [IsAuthenticated,IsAdminUser]
  parser_classes = [JSONParser]

  def get(self,request,id):
    try:
      response,status = AdminLocationServices.getLocation(id)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response, status=status)


  def put(self,request,id):
    data = request.data.copy()
    currentUser = request.user
    try:
      response,status = AdminLocationServices.updateLocation(data,currentUser,id)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response, status=status)      

  def delete(self,request,id):
    currentUser = request.user
    try:
      response,status = AdminLocationServices.deleteLocation(id,currentUser)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response, status=status)

