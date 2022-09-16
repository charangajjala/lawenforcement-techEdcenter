from rest_framework.status import *
from students.serializers import *
from users.models import  *
from students.models import *


class StandardStudentServices:
  @classmethod
  def createStudent(cls,data):
    studentRequest =StandardStudentRequest(data=data)
    if studentRequest.is_valid():
      print('Student Details are valid',studentRequest.validated_data)
      validData = studentRequest.validated_data

      userId = validData.pop('userId',None)
      userObj = User.objects.get(id=userId)

      docs = validData.pop('docs',None)

      student = Student.objects.create(
        **dict(
          validData,
          user=userObj
        )
      )

      if docs:
        for doc in docs:
            docObj = File.objects.get(id=doc.get('id'))
            if doc.get('action') == 'ADD':
                student.docs.add(docObj)
            if doc.get('action') == 'REMOVE':
                student.docs.remove(docObj)

      studentResponse = StandardStudentResponse(student)
      response = studentResponse.data
      status = HTTP_201_CREATED

    else:
      print('data is invalid')
      print(studentRequest.errors)
      response = studentRequest.errors
      status = HTTP_400_BAD_REQUEST
    
    return response,status


  @classmethod
  def getProfile(cls,user):
    try:
      student = Student.objects.get(user = user)
      profile = StandardStudentResponse(student)
      response = profile.data
      status = HTTP_200_OK
    except Student.DoesNotExist:
      response, status = dict(error = "Student not found"), HTTP_404_NOT_FOUND
    except Student.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Students found"), HTTP_400_BAD_REQUEST
    finally:
      return response,status
 
  @classmethod
  def getStudent(cls,id):
    try:
      student=Student.objects.get(id=id)
      profile = StandardStudentResponse(student)
      response = profile.data
      status = HTTP_200_OK
    except Student.DoesNotExist:
      response, status = dict(error = "Student not found"), HTTP_404_NOT_FOUND
    except Student.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Students found"), HTTP_400_BAD_REQUEST
    finally:
      return response,status

  @classmethod
  def updateProfile(cls,data,user):
    global response,status 
    response = None
    status = None
    studentRequest = StudentRequest(data=data,partial=True)
    try:
      if studentRequest.is_valid():
        print('Student Detals are valid',studentRequest.validated_data)
        validData = studentRequest.validated_data

        student = Student.objects.get(user = user)
        oldValues = {}

        docs = validData.pop('docs',None)

        for(k,v) in validData.items():
          oldValues[k] = getattr(student,k)
          setattr(student,k,v)

        if docs:
            if student.docs:
                for (k,v) in docs.items():
                    oldValues[k] = getattr(student.docs,k)
                    setattr(student.docs, k,v)
            else:
              for doc in docs:
                docObj = File.objects.get(id=doc.get('id'))
                if doc.get('action') == 'ADD':
                    student.docs.add(docObj)
                if doc.get('action') == 'REMOVE':
                    student.docs.remove(docObj)

        student.update(oldValues)
        studentResponse = StandardStudentResponse(student)
        response = studentResponse.data
        status = HTTP_200_OK

      else:
        print('Student Data Invalid')       
        print(studentRequest.errors)
        response = studentRequest.errors
        status = HTTP_400_BAD_REQUEST

    except Student.DoesNotExist:
      response, status = dict(error = "Student not found"), HTTP_404_NOT_FOUND

    except Student.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Students found"), HTTP_400_BAD_REQUEST
        print("Multiple Students with one id, WTF!!")
    finally:
      return response,status