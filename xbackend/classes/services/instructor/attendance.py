from rest_framework.status import *
from django.db.models.query_utils import Q

from classes.serializers import AttendanceCodeRequest
from classes.models import Class,Roster
from students.models import Student
from classes.serializers.instructor import UpdateStudentAttendance

class AttendanceSerivices:
  @classmethod
  def attendance(cls,id,code):
    attendanceRequest = AttendanceCodeRequest(data=code)
    if attendanceRequest.is_valid():
      validData =attendanceRequest.validated_data
      try:
        classObj = Class.objects.get(id=id)
        attendanceCode = validData.get('attendanceCode')
        setattr(classObj,'attendanceCode',attendanceCode)
        classObj.save()
        response,status = dict(message = 'Attendance code uploaded'),HTTP_200_OK
      except Class.DoesNotExist:
        response,status = dict(error = 'The requested class is not found'),HTTP_400_BAD_REQUEST
      except Class.MultipleObjectsReturned:
        response,status = dict(error = 'There multiple classes with the same id'),HTTP_400_BAD_REQUEST
    else:
      response,status = attendanceRequest.errors,HTTP_400_BAD_REQUEST
    return response,status 

  @classmethod
  def updateAttendance(cls,id,data):
    studentIdRequest = UpdateStudentAttendance(data=data)
    try:
      if studentIdRequest.is_valid():
        validData = studentIdRequest.validated_data
        studentId = validData.pop('studentId')
        classObj = Class.objects.get(id=id)
        studentObj = Student.objects.get(id=studentId)
        rosterObj = Roster.objects.get(Q(cls=classObj) & Q(student=studentObj))
        setattr(rosterObj,'attendance',True)
        rosterObj.save()
        response,status = dict(message='Student attendance from the instructor has been done'),HTTP_200_OK
      else:
        print('Data Invalid')
        response,status = studentIdRequest.errors,HTTP_400_BAD_REQUEST
    except Class.DoesNotExist:
      response,status = dict(error = 'The requested class is not found'),HTTP_400_BAD_REQUEST
    except Class.MultipleObjectsReturned:
      response,status = dict(error = 'There multiple classes with the same id'),HTTP_400_BAD_REQUEST
    return response,status