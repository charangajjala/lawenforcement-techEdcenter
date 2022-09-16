from collections import OrderedDict

from rest_framework.status import *
from django.forms.models import model_to_dict

from classes.models import Roster,Class
from classes.serializers import StudentCurrentClassResponse,StudentPastClassResponse,StudentTracksResponse
from students.models import Student
from courses.serializers import TrackCourseResponse
from courses.models import CertificationTrack as Track
from courses.models import Course

from datetime import datetime

class StudentClassServices:
  @classmethod
  def current(cls,user):
    try:
      studentObj = Student.objects.get(user=user)
      rosterObjs = Roster.objects.filter(student=studentObj)
      currentClasses=[]
      for roster in rosterObjs:
        classObj = getattr(roster,'cls')
        today = datetime.now()
        endDate = getattr(classObj,'endDate')
        endTime = getattr(classObj,'endTime')
        day =datetime.combine(endDate,endTime)
        #print('\n\n\n',today,'              ',day,'\n\n\n')
        if day>=today:
          currentClasses.append(roster)
        #print('\n\n\n',currentClasses,'\n\n\n')
      classes = StudentCurrentClassResponse(currentClasses,many=True)
      response,status = classes.data,HTTP_200_OK
    except Student.DoesNotExist:
      response,status = dict('This user is not a student'),HTTP_400_BAD_REQUEST
    except Student.MultipleObjectsReturned:
      response,status = dict('There are multiple student to same user'),HTTP_400_BAD_REQUEST
    return response,status
    

  @classmethod
  def past(cls,user):
    try:
      studentObj = Student.objects.get(user=user)
      rosterObjs = Roster.objects.filter(student=studentObj)
      pastClasses=[]
      for roster in rosterObjs:
        classObj = getattr(roster,'cls')
        today = datetime.now()
        endDate = getattr(classObj,'endDate')
        endTime = getattr(classObj,'endTime')
        day =datetime.combine(endDate,endTime)
        #print('\n\n\n',today>=day,'\n\n\n')
        if today>=day:
          pastClasses.append(classObj)
      #print('\n\n\n',pastClasses,'\n\n\n')
      #print('These are past classes : ',pastClasses)
      classes = StudentPastClassResponse(pastClasses,many=True,context={'user':studentObj})
      response,status = classes.data,HTTP_200_OK
      #print('This is the response',response)
    except Student.DoesNotExist:
      response,status = dict('This user is not a student'),HTTP_400_BAD_REQUEST
    except Student.MultipleObjectsReturned:
      response,status = dict('There are multiple student to same user'),HTTP_400_BAD_REQUEST
    return response,status

class StudentTrackServices:
  @classmethod
  def getTracks(cls,user):
    try:
      studentObj = Student.objects.get(user=user)
      rosterObjs = Roster.objects.filter(student=studentObj)
      if len(list(rosterObjs)) != 0:
        trackObjs = Track.objects.filter(isActive=True)
        completedCourses = []
        rRemainingCourses = []
        oRemainingCourses = []
        for roster in rosterObjs:
          classId = roster.cls.id
          courseId = roster.cls.course.id
          classObj = Class.objects.get(id=classId)
          classCourseObj = Course.objects.get(id=courseId)
          if roster.attendance == True and datetime.combine(classObj.endDate,classObj.endTime) < datetime.now():
            for track in trackObjs:
              trackData = TrackCourseResponse(track).data
              requiredCourses = trackData.get('requiredCourses')
              optionalCourses = trackData.get('optionalCourses')
              for course in requiredCourses:
                if course.get('id')  == classCourseObj.id:
                  if course not in completedCourses:
                    completedCourses.append(course)
                else:
                  if course not in rRemainingCourses:
                    rRemainingCourses.append(course)
              for course in optionalCourses:
                if course.get('id')  == classCourseObj.id:
                  if course not in completedCourses:
                    completedCourses.append(course)
                else:
                  if course not in oRemainingCourses:
                    oRemainingCourses.append(course)
          else:
            for track in trackObjs:
              trackData = TrackCourseResponse(track).data
              requiredCourses = trackData.get('requiredCourses')
              optionalCourses = trackData.get('optionalCourses')
              for course in requiredCourses:
                if course not in rRemainingCourses:
                  rRemainingCourses.append(course)
              for course in optionalCourses:
                if course not in oRemainingCourses:
                  oRemainingCourses.append(course)
        for course in rRemainingCourses or oRemainingCourses:
          if course in completedCourses:
            if course in rRemainingCourses:
              rRemainingCourses.remove(course)
            else:
              oRemainingCourses.remove(course)
        #print('These are completed tracks\n\n\n',completedCourses,'\n\n\n')
        studentTrackResponse = StudentTracksResponse(
          trackObjs,
          many=True,
          context={
            'completed':completedCourses,
            'rRemaining':rRemainingCourses,
            'oRemaining':oRemainingCourses,
            'endDate':classObj.endDate,
          })
        response,status = studentTrackResponse.data,HTTP_200_OK
      else:
        response,status = [],HTTP_200_OK
    except Student.DoesNotExist:
      response,status = dict(message='This user is not a student'),HTTP_400_BAD_REQUEST
    except Student.MultipleObjectsReturned:
      response,status = dict(message='There are multiple student to same user'),HTTP_400_BAD_REQUEST
    except Roster.DoesNotExist:
      response,status = dict(message='This user is not registered in any class'), HTTP_200_OK
    except Roster.MultipleObjectsReturned:
      response,status = dict(message='There are multiple student to same user'),HTTP_400_BAD_REQUEST
    return response,status
