from django.http import HttpResponse, JsonResponse
from django.core.exceptions import ValidationError
from django.conf import settings

from rest_framework.views import APIView
from rest_framework.decorators import api_view, parser_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser, FileUploadParser
from rest_framework.status import *

from meta.models import File
from courses.serializers import *
from courses.services import CourseService

class CoursesAPI(APIView):

    def get(self,request):
        params = request.query_params
        response,status = CourseService.getAll2(params)
        return JsonResponse(response,safe=False,status=status)

class CourseAPI(APIView):

    def get(self,request,id):
        response,status = CourseService.getCourse(id)
        return JsonResponse(response,safe=False,status=status)

class FilesAPI(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    parser_classes = [MultiPartParser]

    def post(self, request):
        currentUser = request.user
        #print('This is content type : ',request.headers['Content-Type'])
        #print('this is data that has reached here : ',request.data['file'])
        try:
            datafile = request.data['file']
            material = File.objects.create(
                name = datafile.name,
                file = datafile,
                createdBy = currentUser
            )
            #material.save()
            response, status = material.toAdminDict(), HTTP_201_CREATED
        except Exception as e:
            print('This is the error :',e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        return JsonResponse(response, status=status)
        #return Response(response, status=status, headers='multipart/form-data')
    
    #requires id but id not there in the query
    #not completed verify once again
    def delete(self, request, id):
        currentUser = request.user

        try:
            material = File.objects.get(id=id)
            material.delete(currentUser=currentUser)

            response, status = dict(message="File deleted"), HTTP_200_OK
        except File.DoesNotExist:
            response, status = dict(error="File not found"), HTTP_400_BAD_REQUEST
        except Exception as e:
            print(e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        finally:
            return JsonResponse(response, status=status)

class UiFilesAPI(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        currentUser = request.user
        #print('This is content type : ',request.headers['Content-Type'])
        #print('this is data that has reached here : ',request.data['file'])
        try:
            datafile = request.data['file']
            material = File.objects.create( 
                name = datafile.name,
                file = datafile,
                createdBy = currentUser
            )
            print('material Genarated')
            #material.save()
            response, status = material.toAdminDict(), HTTP_201_CREATED
        except Exception as e:
            print('This is the error :',e)
            response, status = e.__dict__, HTTP_500_INTERNAL_SERVER_ERROR
        return JsonResponse(response, status=status)




