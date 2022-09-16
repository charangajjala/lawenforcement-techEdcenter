from django.http import response
from rest_framework.status import *

from django.db.models.query_utils import Q
from django.forms import model_to_dict

from classes.models import Class,Roster
from students.models import Student

class StudentAttendanceServices:

  @classmethod
  def verify(cls,id,user,attendanceCode):
    try:
      classObj = Class.objects.get(id=id)
      originalAttendanceCode = classObj.attendanceCode
      studentObj = Student.objects.get(user=user)
      rosterObj = Roster.objects.get(Q(cls = classObj)&Q(student=studentObj))
      if int(attendanceCode) == originalAttendanceCode:
        setattr(rosterObj,'attendance',True)
      else:
        response,status = dict(error ='The attendance Coed submitted does not match try again'),HTTP_400_BAD_REQUEST
        return response,status
      rosterObj.save()
      response,status = dict(message='AttendanceCode is verifed and you have attended'),HTTP_200_OK
    except Class.DoesNotExist:
      response,status = dict(error='Requested Class Does Not Exit'),HTTP_400_BAD_REQUEST
    except Student.DoesNotExist:
      response,status = dict(error='Current User is not a student'),HTTP_400_BAD_REQUEST
    except Roster.DoesNotExist:
      response,status = dict(error=' No roster is found for the student and class'),HTTP_400_BAD_REQUEST
    return response,status

class AdminStudentSignInServices:
  @classmethod
  def markPresent(cls,id,data):
    try:
      classObj = Class.objects.get(id=id)
      studentId = data.get('studentId')
      studentObj = Student.objects.get(id=studentId)
      rosterObj = Roster.objects.get(Q(cls=classObj)&Q(student=studentObj))
      setattr(rosterObj,'attendance',True)
      rosterObj.save()
      response,status = dict(message='Student attendance modified successfully'),HTTP_200_OK
    except Class.DoesNotExist:
      response,status = dict(error='Requested Class Does Not Exit'),HTTP_400_BAD_REQUEST
    except Roster.DoesNotExist:
      response,status = dict(error=' No roster is found for the student and class'),HTTP_400_BAD_REQUEST
    return response,status