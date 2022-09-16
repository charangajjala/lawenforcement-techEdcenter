from rest_framework.views import APIView
from rest_framework.parsers import JSONParser
from rest_framework.status import *
from rest_framework.permissions import IsAuthenticated

from django.http.response import JsonResponse

from hosts.services import StandardLocationServices

class StandardLocationsView(APIView):

  parser_classes = [JSONParser] 

  def post(self,request):
    data = request.data
    try:
      response,status = StandardLocationServices.createLocation(data)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response,safe=False, status=status)

  def get(self,request):
    try:
      response,status = StandardLocationServices.getLocations()
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response,safe=False,status=status)

class StandardLocationView(APIView):

  permission_classes = [IsAuthenticated]
  parser_classes = [JSONParser] 

  def put(self,request,id):
    data = request.data
    user = request.user
    try:
      response,status = StandardLocationServices.updateLocation(data,user,id)
    except Exception as e:
      print(e)
      response,status = e.__dict__,HTTP_500_INTERNAL_SERVER_ERROR

    finally:
      return JsonResponse(response,safe=False,status=status)

  def get(self,request,id):
    try:
      response,status = StandardLocationServices.getLocation(id)
    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response, status=status)