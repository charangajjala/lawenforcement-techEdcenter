from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.core.files import File

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser
from rest_framework.status import *

from courses.models import CertificationTrack as Track
from courses.models import Course
from courses.services import *
      
class AdminTrackAPI(APIView):
    """
        URL: /admin/courses/tracks/
        Methods Allowed: GET, PUT, DELETE
        Authorization: JWT Token
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def put(self, request, id):
        data = request.data.copy()
        currentUser = request.user

        try:
            response,status = AdminTrackServices.updateTrack(id,data,currentUser)

        except Exception as e:
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            return JsonResponse(response, status=status)

    def delete(self, request, id):
        currentUser = request.user
        try:
            response,status = AdminTrackServices.deleteTrack(id,currentUser)

        except Exception as e:
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            return JsonResponse(response, status=status)

    def get(self, request, id):
        print('<---- courses.views.AdminTrackAPI.get ---->')
        try:
            response, status = AdminTrackServices.getTrack(id)

        except Exception as e:
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR

        finally:
            return JsonResponse(response, status=status)
        
class AdminTracksAPI(APIView):
    """
        URL: /admin/courses/tracks/
        Methods Allowed: GET, POST
        Authorization: JWT Token
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def get(self, request):
        """
            Method - GET
            Returns a list of certification tracks
        """
        print('<---- courses.views.AdminTracksAPI.get ---->')
        params = self.request.query_params
        response,status = AdminTracksServices.getAllTracks(params)
        return JsonResponse(response,safe=False,status=status)        

    def post(self, request):
        """
            Method - POST
            Creates and returns a Certification Track
        """
        print('<---- courses.views.AdminTracksAPI.post ---->')

        currentUser = request.user
        data = request.data.copy()

        try:
            print('Entering try block')
            response,status = AdminTracksServices.createTrack(data,currentUser)

        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
            
        finally:
            return JsonResponse(response, status=status)

