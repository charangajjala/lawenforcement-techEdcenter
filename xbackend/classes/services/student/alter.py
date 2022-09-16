from django.db.models.query_utils import Q 

from classes.serializers import MoveStudent,RemoveStudent,SubstituteStudent
from students.models import Student
from classes.models import Class,Roster

from rest_framework.status import *

class StudentAlterServices:
  @classmethod
  def move(cls,id,data,user):
    moveRequest = MoveStudent(data=data)
    try:
      if moveRequest.is_valid():
        validData = moveRequest.validated_data
        oldValues={}
        studentId = validData.pop('studentId')
        studentObj=Student.objects.get(id=studentId)
        classId = validData.pop('destClassId')
        classObj = Class.objects.get(id=id)
        destClassObj = Class.objects.get(id=classId)
        rosterObj = Roster.objects.get(Q(cls=classObj)&Q(student=studentObj))
        oldValues['destClassId'] = classId
        oldValues['studentId'] = studentId
        # if rosterObj.attendance == False:
        setattr(rosterObj,'cls',destClassObj)
        rosterObj.update(oldValues,currentUser=user)
        response,status = dict(message='Moved successfully'),HTTP_200_OK
        # else:
        #   if rosterObj.attendance == True:
        #response,status = dict(message ='THe student was accepted to the class can do nothing now'),HTTP_200_OK
      else:
        print('Data Invalid')
        response,status = moveRequest.errors,HTTP_400_BAD_REQUEST

    except Student.DoesNotExist:
      response,status = dict(error='Student does not exist wwith the requested Id'),HTTP_400_BAD_REQUEST
    except Student.MultipleObjectsReturned:
      response,status = dict(error = 'Multiple students with the same ID'),HTTP_400_BAD_REQUEST
    except Class.DoesNotExist:
      response,status = dict(error = 'Class Does not exist with the request Id'),HTTP_400_BAD_REQUEST
    except Class.MultipleObjectsReturned:
      response,status = dict(error='Multiple classes with the same ID'),HTTP_400_BAD_REQUEST
    except Roster.DoesNotExist:
      response,status = dict(error = 'Roster Does not exist with the request Id'),HTTP_400_BAD_REQUEST
    except Roster.MultipleObjectsReturned:
      response,status = dict(error='Multiple rosters with the same ID'),HTTP_400_BAD_REQUEST
    return response,status
  
  @classmethod
  def remove(cls,id,data,user):
    removeRequest = RemoveStudent(data=data)
    try:
      if removeRequest.is_valid():
        validData = removeRequest.validated_data
        studentId = validData.pop('studentId')
        studentObj = Student.objects.get(id=studentId)
        classObj = Class.objects.get(id=id)
        rosterObj = Roster.objects.get(Q(cls=classObj)&Q(student=studentObj))
        if rosterObj.attendance == False:
          setattr(rosterObj,'isDeleted',True)
          rosterObj.delete(currentUser=user)
          response,status = dict(message='removed successfully'),HTTP_200_OK
        else:
          if rosterObj.attendance == True:
            response,status = dict(error ='The student was accepted to the class can do nothing now'),HTTP_400_BAD_REQUEST    
      else:
        print('data Invvalid',removeRequest.errors)
        response,status = dict(error = 'Remove request is not a valid one'),HTTP_400_BAD_REQUEST

    except Student.DoesNotExist:
      response,status = dict(error='Student does not exist wwith the requested Id'),HTTP_400_BAD_REQUEST
    except Student.MultipleObjectsReturned:
      response,status = dict(error='Multiple students with the same ID'),HTTP_400_BAD_REQUEST
    except Class.DoesNotExist:
      response,status = dict(error='Class Does not exist with the request Id'),HTTP_400_BAD_REQUEST
    except Class.MultipleObjectsReturned:
      response,status = dict(error='Multiple classes with the same ID'),HTTP_400_BAD_REQUEST
    except Roster.DoesNotExist:
      response,status = dict(error='Roster Does not exist with the request Id'),HTTP_400_BAD_REQUEST
    except Roster.MultipleObjectsReturned:
      response,status = dict(error='Multiple rosters with the same ID'),HTTP_400_BAD_REQUEST
    return response,status
  
  @classmethod
  def substitute(cl,id,data,user):
    substituteRequest=SubstituteStudent(data=data)
    try:
      if substituteRequest.is_valid():
        validData = substituteRequest.validated_data
        oldValues={}
        for k,v in validData.items():
          oldValues[k] = v
        studentId = validData.pop('studentId')
        studentObj = Student.objects.get(id=studentId)
        newStudentId = validData.pop('newStudentId')
        newStudentObj = Student.objects.get(id=newStudentId)
        classObj=Class.objects.get(id=id)
        rosterObj=Roster.objects.get(Q(cls=classObj)&Q(student=studentObj))
        if rosterObj.attendance == False:
          setattr(rosterObj,'student',newStudentObj)
          rosterObj.update(oldValues,currentUser=user)
          response,status = dict(message='substituted successfully'),HTTP_200_OK
        else:
          if rosterObj.attendance == True:
            response,status = dict(error ='THe student was accepted to the class can do nothing now'),HTTP_400_BAD_REQUEST 
      else:
        print('InvalidData',substituteRequest.errors)
        response,status= dict(error='Substitute request is not a valid one'),HTTP_400_BAD_REQUEST

    except Student.DoesNotExist:
      response,status = dict(error='Student does not exist wwith the requested Id'),HTTP_400_BAD_REQUEST
    except Student.MultipleObjectsReturned:
      response,status = dict(error='Multiple students with the same ID'),HTTP_400_BAD_REQUEST
    except Class.DoesNotExist:
      response,status = dict(error='Class Does not exist with the request Id'),HTTP_400_BAD_REQUEST
    except Class.MultipleObjectsReturned:
      response,status = dict(error='Multiple classes with the same ID'),HTTP_400_BAD_REQUEST
    except Roster.DoesNotExist:
      response,status = dict(error='Roster Does not exist with the request Id'),HTTP_400_BAD_REQUEST
    except Roster.MultipleObjectsReturned:
      response,status = dict(error='Multiple rosters with the same ID'),HTTP_400_BAD_REQUEST
    return response,status
