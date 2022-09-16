import random

from rest_framework.status import *

from classes.serializers import *
from classes.models import Class,Invoice,Roster
from courses.models import Course
from instructors.models import Instructor
from hosts.models import Host,Location
from meta.models import File,Note
from users.models import User
from students.models import Student

from django.contrib.auth.hashers import make_password

class AdminClassServices:
  @classmethod
  def createClass(cls,data,user):
    createRequest = AdminClassRequest(data=data)
    try:
      if createRequest.is_valid():
        validData = createRequest.validated_data
        print(validData)

        courseId = validData.pop('course')
        courseObj = Course.objects.get(id=courseId)
        instructorId = validData.pop('instructor')
        instructorObj = Instructor.objects.get(id=instructorId)
        hostId = validData.pop('host',None)
        locationId = validData.pop('location',None)
        docs = validData.pop('docs',None)
        adminDocs = validData.pop('adminDocs',None)
        adminNotes = validData.pop('adminNotes',None)
        aar = validData.pop('aar',None)
        if hostId == None or locationId == None:
          classObj=Class.objects.create(
              **dict(
                validData,
                course = courseObj,
                instructor = instructorObj,
                createdBy = user
            )
          )
        else:
          hostObj = Host.objects.get(id=hostId)
          locationObj = Location.objects.get(id=locationId)
          classObj=Class.objects.create(
              **dict(
                validData,
                course = courseObj,
                host=hostObj,
                location=locationObj,
                instructor = instructorObj,
                createdBy = user
            )
          )

        if docs:
            classObj.docs.add(*File.objects.filter(id__in=[doc.get('id') for doc in docs]))
        if adminDocs:
          classObj.adminDocs.add(*File.objects.filter(id__in=[doc.get('id') for doc in adminDocs]))
        if adminNotes:
            for note in adminNotes:
                classObj.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=user)))
        if aar:
          setattr(classObj,'aar',aar)

        classResponse = AdminClassResponse(classObj)
        response,status = classResponse.data,HTTP_201_CREATED
      else:
        print("Invalid Data : ",data)
        print(createRequest.errors)
        response, status = createRequest.errors, HTTP_400_BAD_REQUEST
    except Course.DoesNotExist:
      response,status = dict(error = 'request Course does not exist'),HTTP_400_BAD_REQUEST
    except Course.MultipleObjectsReturned:
      response,status = dict(error = 'multiple objects returned for the same Course'),HTTP_400_BAD_REQUEST
    except Instructor.DoesNotExist:
      response,status = dict(error = 'request Instructor does not exist'),HTTP_400_BAD_REQUEST
    except Instructor.MultipleObjectsReturned:
      response,status = dict(error = 'multiple objects returned for the same Instructor'),HTTP_400_BAD_REQUEST
    except Host.DoesNotExist:
      response,status = dict(error = 'request Host does not exist'),HTTP_400_BAD_REQUEST
    except Host.MultipleObjectsReturned:
      response,status = dict(error = 'multiple objects returned for the same Host'),HTTP_400_BAD_REQUEST
    except Location.DoesNotExist:
      response,status = dict(error = 'request Location does not exist'),HTTP_400_BAD_REQUEST
    except Location.MultipleObjectsReturned:
      response,status = dict(error = 'multiple objects returned for the same Location'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def updateClass(cls,id,data,user):
    updateRequest = AdminClassRequest(data=data,partial=True)
    try:
      if updateRequest.is_valid():
        validData = updateRequest.validated_data
        oldValues={}
        docs = validData.pop('docs',None)
        adminDocs = validData.pop('adminDocs',None)
        adminNotes = validData.pop('adminNotes',None)
        aar = validData.pop('aar',None)

        instructorId = validData.pop('instructor',None)
        hostId = validData.pop('host',None)
        locationId = validData.pop('location',None)
        courseId = validData.pop('course',None)


        classObj = Class.objects.get(id=id)

        if hostId:
          hostObj = Host.objects.get(id=hostId)
          setattr(classObj,'host',hostObj)

        if locationId:
          locationObj = Location.objects.get(id=locationId)
          setattr(classObj,'location',locationObj)    

        if instructorId:
          instructorObj = Instructor.objects.get(id=instructorId)
          setattr(classObj,'instructor',instructorObj)
        
        if courseId:
          courseObj = Course.objects.get(id=courseId)
          setattr(classObj,'course',courseObj)
          
        for (k, v) in validData.items():
          oldValues[k] =  getattr(classObj, k)
          setattr(classObj, k, v)

        if docs:
            for doc in docs:
                docObj = File.objects.get(id=doc.get('id'))
                if doc.get('action') == 'ADD':
                    classObj.docs.add(docObj)
                if doc.get('action') == 'DELETE':
                    classObj.docs.remove(docObj)
        
        if adminDocs:
            for doc in adminDocs:
                docObj = File.objects.get(id=doc.get('id'))
                if doc.get('action') == 'ADD':
                    classObj.adminDocs.add(docObj)
                if doc.get('action') == 'DELETE':
                    classObj.adminDocs.remove(docObj)
        if adminNotes:  
            for note in adminNotes:
                classObj.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=user)))
        if aar:
          setattr(classObj,'aar',aar)

        classObj.update(oldValues,currentUser=user)
        classResponse = AdminClassResponse(classObj)
        response,status = classResponse.data,HTTP_200_OK
      else:
        print("Invalid Data : ",data)
        print(updateRequest.errors)
        response, status = updateRequest.errors, HTTP_400_BAD_REQUEST
    except Class.DoesNotExist:
      response,status = dict(error = 'request Class does not exist'),HTTP_404_NOT_FOUND
    except Class.MultipleObjectsReturned:
      response,status = dict(error = 'multiple objects returned for the same Class'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def deleteClass(cls,id,user):
    try:
      classObj = Class.objects.get(id=id)
      rosterObjs = Roster.objects.filter(ls=classObj)
      for roster in rosterObjs:
        setattr(roster,'isDeleted',True)
      classObj.delete(currentUser=user)
      response,status = dict(message='Class deleted successfully'),HTTP_200_OK
    except Class.DoesNotExist:
      response,status = dict(error = 'request Class does not exist'),HTTP_400_BAD_REQUEST
    except Class.MultipleObjectsReturned:
      response,status = dict(error = 'multiple objects returned for the same Class'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def getClasses(cls,params):
    classObjs = Class.objects.all().order_by('id')
    if params:
      scls = params.get('scls')
      if scls == 'current':
        classObjs = classObjs.exclude(status__in=[4,5])
      if scls == 'past':
        classObjs = classObjs.exclude(status__in=[1,2,3])
      classResponse = AdminClassesResponse(classObjs,many=True)
    else:
      classResponse = AdminClassesResponse(classObjs,many=True)  
    response,status= classResponse.data,HTTP_200_OK
    return response,status
    
  @classmethod
  def getClass(cls,id):
    try:
      classObj = Class.objects.get(id =id)
      classResponse = AdminClassResponse(classObj)
      response,status = classResponse.data,HTTP_200_OK
    except Class.DoesNotExist:
      response,status = dict(error = 'request Class does not exist'),HTTP_400_BAD_REQUEST
    except Class.MultipleObjectsReturned:
      response,status = dict(error = 'multiple objects returned for the same Class'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def addRoster(cls,id,data):
    inServiceRequest = InserviceRosterRequest(data=data,many=True)
    
    if inServiceRequest.is_valid():
      print('Starting process')
      valdiData = inServiceRequest.data
      classObj = Class.objects.get(id=id)
      invocieObj = classObj.inServiceInvoice
      for obj in valdiData:
        email = obj.pop('email',None)
        agency = obj.pop('agency',None)
        try:
          userObj = User.objects.get(email=email)
          studentObj = Student.objects.get(user=userObj)
      
        #what to do if details given are not student
        except User.DoesNotExist:
          #genarating random password to hash it while creating a user
          password=User.objects.make_random_password()
          if obj.get('title'):
        
            userObj = User.objects.create(
              **dict(
                obj,
                password = make_password(password),
                email=email
              )
            )
        
            studentObj = Student.objects.create(
              user = userObj,
              agencyName = agency,
            )
        
          else:
            userObj = User.objects.create(
              **dict(
                obj,
                password = make_password(password),
                email=email
              )
            )
        
            studentObj = Student.objects.create(
              user = userObj,
              agencyName = agency,
            )
        
        Roster.objects.create(
          student=studentObj,
          cls = classObj,
          invoice=invocieObj
        )
    
      response,status = dict(message='student added'),HTTP_200_OK
    else:
      print('Data Invalid',inServiceRequest.errors)
      response,status = dict(error='Request Invalid'),HTTP_400_BAD_REQUEST
    return response,status