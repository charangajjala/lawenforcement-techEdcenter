from rest_framework.views import APIView
from rest_framework.status import *
from django.http import JsonResponse

from courses.services import *
from classes.models import Class
from classes.serializers import ClassesResponse

from django.db.models.query_utils import Q

import datetime


class TracksAPI(APIView):
  def get(self,request):
    response,status = AdminTracksServices.usergetAllTracks()
    return JsonResponse(response,safe=False,status=status)

class TrackAPI(APIView):
  def get(self,request,id):
    print('Enterd here')
    response,status = AdminTrackServices.usergetTrack(id)
    return JsonResponse(response,safe=False,status=status)

class TopicAPI(APIView):
  def get(self,request):
    response,status = TopicServices.topicList()
    return JsonResponse(response,safe=False,status=status)

class UpcomingClasses(APIView):
  def get(self,request,id):
    today = datetime.datetime.now()
    course = Course.objects.get(id = id)
    classes = Class.objects.filter(Q(course = course)&Q(startDate__gt=today))
    classesResponse = ClassesResponse(classes,many=True)
    data = classesResponse.data
    return JsonResponse(data=data,safe=False,status=HTTP_200_OK)

