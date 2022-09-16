from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError

from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser, MultiPartParser, FileUploadParser
from rest_framework.status import *

from courses.services import TopicService

class AdminTopicsAPI(APIView):
    """
        URL: /admin/courses/topics/
        Methods Allowed: GET, POST
        Authorization: JWT Token
    """
    
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def post(self, request):
        """
            Create a Topic
        """
        print("<---- courses.views.AdminTopicsAPI.post ---->")
        currentUser = request.user
        data = request.data.copy()

        try:
            response, status = TopicService.createTopic(data, currentUser)
            
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

    def get(self, request):
        """
            Returns list of all topics
        """
        print("<---- courses.views.AdminTopicsAPI.get ---->")
        params = self.request.query_params
        response, status = TopicService.getAllTopics(params)
        return JsonResponse(response, safe=False, status=status)

class AdminTopicAPI(APIView):
    """
        URL: /admin/courses/topics/<int:id>/
        Methods Allowed: GET, PUT, DELETE
        Authorization: JWT Token
    """

    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def get(self, request, id):
        """
            Get Topic
        """
        print("<---- courses.views.AdminTopic.get ---->")

        try:
            response, status = TopicService.getTopic(id)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

    def put(self, request, id):
        """
            Edit Topic
        """
        print("<---- courses.views.AdminTopicAPI.put ---->")

        currentUser = request.user
        data = request.data.copy()

        try:
            response, status = TopicService.updateTopic(id, data, currentUser)
            
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

    def delete(self, request, id):
        """
            Delete Topic
        """
        print("<---- courses.views.AdminTopic.delete ---->")

        try:
            response, status = TopicService.deleteTopic(id, request.user)
            
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)
