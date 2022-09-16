from django.conf import settings
from django.db.models.query_utils import Q
from django.utils.functional import partition
from rest_framework.status import *

from meta.models import File
from users.models import User

from datetime import *

from courses.models import CertificationTrack,Course
from courses.serializers import TracksListResponse,TrackRequest,TrackResponse


class AdminTracksServices:
  @classmethod
  def getAllTracks(cls,params=None):
    global createdon
    createdon = None
    try:
      if params:
        id = params.get('sid')
        title = params.get('stitle')
        shortName = params.get('sshtname')
        isActive = True if params.get('sactive')=='true' else False if params.get('sactive')=='false' else None
        numCourses = params.get('sncourses')
        created = params.get('screatedat')

        if created:
          createdon = datetime.strptime(created,'%Y-%m-%d')

        tracks = CertificationTrack.objects.all()
        if id:
          tracks = tracks.filter(id=id)
        if numCourses:
          tracks = tracks.filter(numCourses=numCourses)
        if isActive in (True,False):
          tracks = tracks.filter(isActive=isActive)
        if title:
          tracks = tracks.filter(title__startswith=title)
        if shortName:
          tracks = tracks.filter(shortName__startswith=shortName)
        if created:
          tracks = tracks.filter(created__date=created)

      else:
        tracks = CertificationTrack.objects.all()
      tracksResponse = TracksListResponse(tracks,many=True)
      response,status = tracksResponse.data,HTTP_200_OK
    except ValueError:
      response,status = dict(error = "There is some error that i dont know"), HTTP_404_NOT_FOUND
    return response, status

  @classmethod
  def usergetAllTracks(cls):
    tracks = CertificationTrack.objects.all().order_by('title')
    tracksResponse = TrackResponse(tracks,many=True)
    response = tracksResponse.data
    return response,HTTP_200_OK

  @classmethod
  def createTrack(cls,data,currentUser):
    print('Validating Request',data)
    print('Current in user : ',currentUser)
    trackRequest = TrackRequest(data=data,partial=True)
    if trackRequest.is_valid():
      print('Track Data is Valid')
      print(trackRequest.validated_data)

      validData = trackRequest.validated_data
      print('ValidData : ',validData)

      logoId = validData.pop('logo',None)
      logoObj = File.objects.get(id=logoId) if logoId else None
      print('Logo obj is found')

      requiredCourses = validData.pop('requiredCourses',None)
      optionalCourses = validData.pop('optionalCourses',None)

      
      track = CertificationTrack.objects.create(
        **dict(
          validData,
          logo = logoObj,
          createdBy=currentUser,
        )
      )
      print('Track Object created with user ',track.createdBy)

      if requiredCourses:
        for course in requiredCourses:
          courseId = course.get('id')
          courseObj = Course.objects.get(id=courseId)
          if course.get('action') == 'ADD':
            track.requiredCourses.add(courseObj)
          if course.get('action') == 'DELTE':
            track.requiredCourses.remove(courseObj)

      if optionalCourses:
        for course in optionalCourses:
          courseId = course.get('id')
          courseObj = Course.objects.get(id=courseId)
          if course.get('action') == 'ADD':
            track.optionalCourses.add(courseObj)
          if course.get('action') == 'DELETE':
            track.optionalCourses.remove(courseObj)
      print('Courses updated')

      trackResponse = TrackResponse(track)
      response,status = trackResponse.data,HTTP_201_CREATED

    else:
      print('Track Data Invalid')
      response,status = trackRequest.errors,HTTP_400_BAD_REQUEST
    return response,status
        

class AdminTrackServices:

  @classmethod
  def updateTrack(cls,id,data,currentUser):
    trackRequest = TrackRequest(data=data,partial=True)
    try:
      if trackRequest.is_valid():
        print('Track Data is Valid',trackRequest.validated_data)
        oldValues = {}

        validData = trackRequest.validated_data
        track = CertificationTrack.objects.get(id=id)

        logoId = validData.pop('logo',None)
        
        if logoId:
          logoObj = File.objects.get(id=logoId)
          print('New logo Id updated successfully')

        requiredCourses = validData.pop('requiredCourses',None)
        optionalCourses = validData.pop('optionalCourses',None)

        print('items',validData.items())

        for (k, v) in validData.items():
          oldValues[k] =  getattr(track, k)
          setattr(track, k, v)
        print('Updated past value')

        if requiredCourses:
          for course in requiredCourses:
            courseId = course.get('id')
            courseObj = Course.objects.get(id=courseId)
            if course.get('action') == 'ADD':
              track.requiredCourses.add(courseObj)
            if course.get('action') == 'DELETE':
              track.requiredCourses.remove(courseObj)

        if optionalCourses:
          for course in optionalCourses:
            courseId = course.get('id')
            courseObj = Course.objects.get(id=courseId)
            if course.get('action') == 'ADD':
              track.optionalCourses.add(courseObj)
            if course.get('action') == 'DELETE':
              track.optionalCourses.remove(courseObj)
        print('Courses updated')

        track.update(oldValues,currentUser)
        trackResponse = TrackResponse(track)
        response,status = trackResponse.data,HTTP_200_OK
      
      else:
        print('Track Data invalid',trackRequest.errors)
        response,status = trackRequest.errors,HTTP_400_BAD_REQUEST

    except CertificationTrack.DoesNotExist:
      response, status = dict(error = "Track not found"), HTTP_404_NOT_FOUND

    except CertificationTrack.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Tracks found"), HTTP_400_BAD_REQUEST
        print("Multiple Tracks with one id, WTF!!")

    return response, status

  @classmethod
  def deleteTrack(cls,id,currentUser):
    try:
      track = CertificationTrack.objects.get(id=id)
      track.delete(currentUser=currentUser)
      response,status = dict(message="Track Deleted successfully"),HTTP_200_OK

    except CertificationTrack.DoesNotExist:
        response, status = dict(error = "Track not found"), HTTP_404_NOT_FOUND
    except CertificationTrack.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Tracks found"), HTTP_400_BAD_REQUEST
        print("Multiple Tracks with one id, WTF!!")

    return response, status

  @classmethod
  def getTrack(cls,id):
    try:
      track = CertificationTrack.objects.get(id=id)
      trackReponse = TrackResponse(track)
      response,status = trackReponse.data,HTTP_200_OK

    except CertificationTrack.DoesNotExist:
        response, status = dict(error = "Track not found"), HTTP_404_NOT_FOUND

    except CertificationTrack.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Tracks found"), HTTP_400_BAD_REQUEST
        print("Multiple Tracks with one id, WTF!!")

    return response, status

  @classmethod
  def usergetTrack(cls,id):
    try:
      track = CertificationTrack.objects.get(id=id)
      trackReponse = TrackRequest(track)
      response,status = trackReponse.data,HTTP_200_OK

    except CertificationTrack.DoesNotExist:
        response, status = dict(error = "Track not found"), HTTP_404_NOT_FOUND

    except CertificationTrack.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Tracks found"), HTTP_400_BAD_REQUEST
        print("Multiple Tracks with one id, WTF!!")

    return response, status