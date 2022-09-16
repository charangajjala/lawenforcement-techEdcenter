from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from rest_framework.status import *

from courses.services import *

import json

from courses.models import Course, Topic, Agenda
from courses.serializers import *


class AdminCoursesAPI(APIView):
    """
        URL: /admin/courses/
        Methods Allowed: GET, POST
        Authorization: JWT Token
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def get(self, request):
        """
            List of courses
        """
        print("<---- courses.views.courses.AdminCourseAPI ---->")
        params = request.query_params
        response, status = CourseService.getAll(params)
        return JsonResponse(response, safe=False, status=status)    

    def post(self, request):
        """
            Create a course
        """
        print("<---- courses.views.courses.AdminCoursesAPI ---->")
        currentUser = request.user
        data = request.data

        try:
            response, status = CourseService.create(data, currentUser)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

class AdminCourseAPI(APIView):
    """
        URL: /admin/courses/<int:id>/
        Methods Allowed: PUT, GET, DELETE
        Authorization: JWT Token
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def get(self, request, id):
        """
            Get a course
        """
        print("<---- courses.views.courses.AdminCourseAPI.get ---->")

        try:
            response, status = CourseService.getCourse(id)
            print(response, status)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

    def put(self, request, id):
        """
            Edit Course
        """
        print("<---- courses.views.courses.AdminCourseAPI.put ---->")

        currentUser = request.user
        data = request.data
        try:
            response, status = CourseService.update(id, data, currentUser)
        except Exception as e:
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

    def delete(self, request, id):
        """
            Delete course
        """
        print("<---- courses.views.courses.AdminCourseAPI.delete ---->")
        currentUser = request.user

        try:
            response, status = CourseService.delete(id,currentUser)
            print(response, status)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)










