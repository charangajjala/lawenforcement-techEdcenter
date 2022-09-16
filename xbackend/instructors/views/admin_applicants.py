from django.http.response import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from instructors.services import *

class AdminInstructorApplicantsAPI(APIView):

  permission_classes = [IsAuthenticated, IsAdminUser]
  parser_classes = [JSONParser]

  def get(self,request):
    '''
      GET ALL APPLICANTS
    '''
    params = request.query_params
    response, status = AdminApplicantsService.getAllApplicants(params)
    return JsonResponse(response,safe=False,status=status)

class AdminInstructorApplicantAPI(APIView):

  permission_classes = [IsAuthenticated, IsAdminUser]
  parser_classes = [JSONParser]

  def get(self,request,id):
    """
        Get applicant
    """
    try:
        response,status = AdminApplicantsService.getApplicant(id)
        print(response)

    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response, status=status)

  def put(self,request,id):
    """
      Update applicant
    """
    data = request.data.copy()
    currentUser = request.user
    try:
        response,status = AdminApplicantsService.updateApplicant(id,data,currentUser)
        print(response)

    except Exception as e:
        print(e)
        response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

    finally:
        return JsonResponse(response, status=status)

  def delete(self,request,id):
      """
          Delete a user
      """
      currentUser = request.user
      try:
          response, status = AdminApplicantsService.deleteApplicant(id,currentUser )
          print(response, status)
      except Exception as e:
          print(e)
          response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
      finally:
          return JsonResponse(response, status=status)