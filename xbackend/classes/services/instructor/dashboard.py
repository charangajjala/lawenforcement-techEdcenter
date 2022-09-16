from django.core.checks import messages
from django.forms.models import model_to_dict
from rest_framework.status import *

from instructors.models import Instructor
from classes.models import Class,Roster
from classes.serializers import CurrentClassesResponse,PastClassesResponse,CloseClassRequest
from students.models import Student
from meta.models import File

from django.db.models.query_utils import Q

class InstructorDashboardServices:

  @classmethod
  def currentClasses(cls,user):
    try:
      instructorObj = Instructor.objects.get(user=user)
      classObjs = Class.objects.filter(instructor=instructorObj)
      currentClassObjs = []
      for classObj in classObjs:
        if classObj.status != 4:
          currentClassObjs.append(classObj)
      currentClasses = CurrentClassesResponse(currentClassObjs,many=True)
      print(currentClasses.data)
      response,status = currentClasses.data,HTTP_200_OK
    except Instructor.DoesNotExist:
      response,status = dict(error = 'user is not an instructor'), HTTP_400_BAD_REQUEST
    except Instructor.MultipleObjectsReturned:
      response,status = dict(error = 'there are more than one instructor with this user'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def pastClasses(cls,user):
    try:
      instructorObj = Instructor.objects.get(user=user)
      classObjs = Class.objects.filter(instructor=instructorObj)
      pastClassObjs = []   
      for classObj in classObjs:
        if classObj.status == 4:
          pastClassObjs.append(classObj)
      pastClasses = PastClassesResponse(pastClassObjs,many=True)
      response,status = pastClasses.data,HTTP_200_OK
    except Instructor.DoesNotExist:
      response,status = dict(error = 'user is not an instructor'), HTTP_400_BAD_REQUEST
    except Instructor.MultipleObjectsReturned:
      response,status = dict(error = 'there are more than one instructor with this user'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def closeClass(cls,id,data):
    closeClassRequest = CloseClassRequest(data=data)
    if closeClassRequest.is_valid():
      validData = closeClassRequest.validated_data
      classObj = Class.objects.get(id=id)
      allStudentIds =[]
      rosterObjs = Roster.objects.filter(cls=classObj)
      for roster in rosterObjs:
        allStudentIds.append(roster.student.id)
      aarObj = validData.get('aar')
      setattr(classObj,'aar',aarObj)
      attendanceIds = validData.get('attendance')
      docs = validData.pop('docs',None)
      for doc in docs:
        docObj = File.objects.get(id=doc.get('id'))
        if docObj:
          if doc.get('action') == 'ADD':
            classObj.docs.add(docObj)
          elif doc.get('action') == 'DELETE':
            classObj.docs.remove(docObj)
      for id in allStudentIds:
        studentObj = Student.objects.get(id=id)
        rosterObj = Roster.objects.get(Q(cls=classObj)&Q(student=studentObj))
        try:
          if id in attendanceIds:
            setattr(rosterObj,'attendance',True)
          else:
            setattr(rosterObj,'attendance',False)
          rosterObj.save()
        except Student.DoesNotExist:
          response,status = dict(error = 'Student does not exist if wish to create one'),HTTP_400_BAD_REQUEST
        except Student.MultipleObjectsReturned:
          response,status = dict(error = 'Student should actually be non existant'),HTTP_400_BAD_REQUEST
      setattr(classObj,'status',4)#settign class Status to Closed
      classObj.save()
      response,status = dict(message = 'Class closed sucessfully'),HTTP_200_OK
    else:
      response,status = closeClassRequest.errors,HTTP_400_BAD_REQUEST
    return response,status