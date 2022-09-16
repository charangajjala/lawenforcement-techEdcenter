from instructors.services import *
from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser
from rest_framework.status import *


class AdminInstructorsAPI(APIView):
    """
        /admin/instructors/
        GET, POST
        JWT Auth
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def get(self, request):
        """
            List of instructors
        """

        params = request.query_params

        response, status = AdminInstructorService.getAllInstructors(params)
        return JsonResponse(response,safe=False,status=status)

    def post(self, request):
        """
            Create a instructor
        """
        
        currentUser = request.user
        data = request.data

        try:
            response, status = AdminInstructorService.createInstructor(data, currentUser)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)        


class AdminInstructorAPI(APIView):

    """
        URL - /instutors/<int:id>/
        Methods Allowed - GET, PUT, DELETE
        Authorization - JWT Authentication
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def get(self,request,id):
        """
            Get user
        """
        try:
            response,status = AdminInstructorService.getInstructor(id)

        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            return JsonResponse(response, status=status)

    def put(self,request,id):
        """
            Edit user
        """
        currentUser = request.user
        data = request.data.copy()
        try:
            response, status = AdminInstructorService.updateInstructor(id, data, currentUser)
            print(response, status)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)
    
    def delete(self,request,id):
        """
            Delete a user
        """
        try:
            response, status = AdminInstructorService.deleteInstructor(id, request.user)
            print(response, status)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)