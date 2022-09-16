from django.core.checks import messages
from classes.serializers import DocsRequest,DocsUploadRequest
from classes.models import Class,Roster
from meta.models import File
from courses.models import Course
from instructors.models import Instructor
from classes.serializers import CourseDocsResponse

from rest_framework.status import *

class InstructorDocServices:

  @classmethod
  def uploadDocs(cls,id,data):
    docUploadRequest = DocsUploadRequest(data=data)
    if docUploadRequest.is_valid():
        validData = docUploadRequest.validated_data
        docs = validData.pop('docs',None)
        try:
          classObj = Class.objects.get(id=id)
          for doc in docs:
              docObj = File.objects.get(id=doc.get('id'))
              if docObj:
                  if doc.get('action') == 'ADD':
                    classObj.docs.add(docObj)
                  elif doc.get('action') == 'DELETE':
                    classObj.docs.remove(docObj)
          classObj.save()
          response,status = dict(message = 'File uploaded successfully'),HTTP_200_OK
        except File.DoesNotExist:
          response,status = dict(error='There is no such file'),HTTP_400_BAD_REQUEST
        except File.MultipleObjectsReturned:
          response,status = dict(error = 'Thats not possible'),HTTP_400_BAD_REQUEST
    else:
      print('Data Invalid')
      response,status = docUploadRequest.errors,HTTP_400_BAD_REQUEST
    return response,status

class CourseDocServices:

  @classmethod
  def getCourseDocs(cls,user,courseId):
    try:
      instructorObj = Instructor.objects.get(user=user)
      classObjs = Class.objects.filter(instructor=instructorObj).order_by('course_id')
      courseObjs = []

      for classObj in classObjs:
        courseId = classObj.course.id
        courseObj = Course.objects.get(id=courseId)
        if courseObj:
          courseObjs.append(courseObj)
      
      courseObjserializer = CourseDocsResponse(courseObjs,many=True)
      response,status = courseObjserializer.data,HTTP_200_OK
    except Instructor.DoesNotExist:
      response,status = dict(error = 'The user is not an instructor'),HTTP_400_BAD_REQUEST
    except Instructor.MultipleObjectsReturned:
      response,status = dict(error = 'Multiple instrcutors should not be there'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def uploadCoursedocs(cls,data,courseId):
    courseDocsuploadRequest = DocsUploadRequest(data=data)
    if courseDocsuploadRequest.is_valid():
      validData = courseDocsuploadRequest.validated_data
      docs = validData.pop('docs',None)
      course = Course.objects.get(id=courseId)
      if docs:
        for doc in docs:  
          docObj = File.objects.get(id=doc.get('id'))
          if doc.get('action') == 'ADD':
              course.material.add(docObj)
          elif doc.get('action') == 'DELETE':
              course.material.remove(docObj)
      response,status = dict(message = 'Course Documents Uploaded'),HTTP_200_OK
    else:
      print('Data Invalid')
      print(courseDocsuploadRequest.errors)
      response,status = courseDocsuploadRequest.errors,HTTP_400_BAD_REQUEST
    return response,status


      
