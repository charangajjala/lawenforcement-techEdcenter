from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser

from django.http.response import JsonResponse


from instructors.serializers import *
from instructors.services import *

SAFE_METHODS = ['POST']

class IsAuthenticated(BasePermission):
    """
    The request is authenticated as a user, or not a user request.
    """

    def has_permission(self, request, view):
        if (request.method in SAFE_METHODS):
            return False
        return True


class InstructorApplicantsAPI(APIView):

  parser_classes = [JSONParser]

  def post(self,request):

    data = request.data
    try:
      response, status = InstructorApplicantServices.createApplicant(data)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
      return JsonResponse(response,status=status)

  def put(self,request):
    
    user = request.user
    data = request.data
    try:
      response,status = InstructorApplicantServices.updateApplicant(user,data)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return JsonResponse(response,safe=False, status=status)

  def get(self,request):

    user = request.user
    try:
      response,status = InstructorApplicantServices.getApplicant(user)
    except Exception as e:
      print(e)
      response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
    finally:
        return JsonResponse(response,safe=False, status=status)