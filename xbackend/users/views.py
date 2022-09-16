from django.db.utils import IntegrityError
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import JSONParser
from rest_framework.status import *

from .services import UserService,StandardUserServices

class UsersAPI(APIView):
    """
        URL: /users/
        Methods Allowed: GET, POST
        Authorization: JWT Token
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def get(self, request):
        """
            Returns a list of all users
        """
        print("<---- users.views.UsersAPI.get ---->")

        params = self.request.query_params

        response, status = UserService.getAllUsers(params)
        return JsonResponse(response, safe=False, status=status)

    def post(self, request):
        """
            Creates and returns a user
        """
        print("<---- users.views.UsersAPI.post ---->");
        currentUser = request.user
        data = request.data.copy()

        try:
            response, status = UserService.createUser(data, currentUser)

        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

class UserAPI(APIView):
    """
        URL - /users/<int:id>/
        Methods Allowed - GET, PUT, DELETE
        Authorization - JWT Authentication
    """
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [JSONParser]

    def get(self, request, id):
        """
            Get user
        """
        print("<---- users.views.UserAPI.get ---->");

        try:
            response, status = UserService.getUser(id)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

    def put(self, request, id):
        """
            Edit user
        """
        print("<---- users.views.UserAPI.put ---->");

        currentUser = request.user
        data = request.data.copy()

        try:
            response, status = UserService.updateUser(id, data, currentUser)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

    def delete(self, request, id):
        """
            Delete a user
        """
        print("<---- users.views.UserAPI.delete ---->");

        try:
            response, status = UserService.deleteUser(id, request.user)
            print(response, status)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

class StandardUserAPI(APIView):

    permission_classes = [IsAuthenticated]

    def get(self,request):
        currentUser = request.user

        try:
            response, status = StandardUserServices.getUser(currentUser)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status,safe=False)


    def post(self,request):
        data =request.data.copy()

        try:
            response,status = StandardUserServices.createUser(data)
        except Exception as e:  
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response,status=status)

    def put(self,request):

        currentUser = request.user
        data = request.data.copy()

        try:
            response, status = StandardUserServices.updateUser(data, currentUser)
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

class UserListAPI(APIView):
    def get(self,request):
        try:
            response,status = StandardUserServices.getListofUsers()
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status,safe=False)        