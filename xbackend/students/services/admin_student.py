from functools import partial
from rest_framework.status import *
from students.models import *
from students.serializers import *

from datetime import *

from django.db.models.query_utils import Q

from users.models import *

class AdminStudentsServices:
  @classmethod
  def getAllStudents(cls,params):
    global createdon,user
    createdon = None
    if params:
      isActive = True if params.get('sactive')=='true' else False if params.get('sactive')=='false' else None
      id = params.get('sid')
      agencyName = params.get('sagencyname')
      email = params.get('semail')
      lastName = params.get('slname')
      firstName = params.get('sfname')
      created = params.get('screatedat')

      if created:
        createdon = datetime.strptime(created,'%Y-%m-%d')

      if firstName or email or lastName:
        users = User.objects.all()
        if firstName:
            users = users.filter(firstName__startswith=firstName)
        if lastName:
            users = users.filter(lastName__startswith=lastName)
        if email:
            users = users.filter(email=email)

      students = Student.objects.all()
      if id:
        students = students.filter(id=id)
      if isActive:
        students = students.filter(isActive=isActive)
      if agencyName:
        students = students.filter(agencyName__startswith=agencyName)
      if createdon:
        students = students.filter(created__date = createdon)
      if users:
        students = students.filter(user__in=users)
        
    else:
      students = Student.objects.only('user','agencyName')

    print('all the student objects are captured')
    studentResponse = StudentsListResponse(students,many=True)
    response = studentResponse.data
    print(response)
    status = HTTP_200_OK
    return response,status

  @classmethod
  def createStudent(cls,currentUser,data):
    studentRequest = StudentRequest(data=data)
    if studentRequest.is_valid():
      print('Student Data is Valid',studentRequest.validated_data)
      validData = studentRequest.validated_data

      userId = validData.pop('userId',None)
      userObj = User.objects.get(id=userId)
      
      docs = validData.pop('docs',None)
      adminNotes = validData.pop('adminNotes',None)
      print('Student object about to be created')

      student = Student.objects.create(
        **dict(
          validData,
          user =userObj,
          createdBy = currentUser
        )
      )
      print('Student object created')
      print('adminNotes',adminNotes)

      if docs:
        student.docs.add(*File.objects.filter(id__in=[doc.get('id') for doc in docs]))

      if adminNotes:
        for note in adminNotes:
            student.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=currentUser)))
      print('Student Genarated')
      studentResponse = StudentResponse(student)
      response = studentResponse.data
      print('Student Response Genarated')
      status = HTTP_201_CREATED

    else:
      print('data is invalid')
      print(studentRequest.errors)
      response = studentRequest.errors
      status = HTTP_400_BAD_REQUEST
    
    return response,status

      
class AdminStudentServices:
  @classmethod
  def getStudentProfile(cls,id):
    try:
      studentObj = Student.objects.get(id=id)
      profile = StudentResponse(studentObj)
      response = profile.data
      status = HTTP_200_OK
    except Student.DoesNotExist:
      response, status = dict(error = "Student not found"), HTTP_404_NOT_FOUND
    except Student.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Students found"), HTTP_400_BAD_REQUEST
    finally:
      return response,status

  @classmethod
  def updateStudentProfile(cls,id,currentUser,data):
    studentRequest = StudentRequest(data=data,partial=True)
    try:
      if studentRequest.is_valid():
        print('Data is validated',studentRequest.validated_data)
        validData = studentRequest.validated_data
        oldValues = {}

        student = Student.objects.get(id=id)
        docs = validData.pop('docs',None)
        adminNotes =validData.pop('adminNotes',None)


        for(k,v) in validData.items():
          oldValues[k] = getattr(student,k)
          setattr(student,k,v)

        if docs:
            student.docs.add(*File.objects.filter(id__in=[doc.get('id') for doc in docs]))

        if adminNotes:
          for note in adminNotes:
            student.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=currentUser)))

        student.update(oldValues,currentUser)
        studentResponse = StudentResponse(student)
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

    return response,status                     

  @classmethod
  def deleteStudent(cls,id,currentUser):
    try:
      student = Student.objects.get(id=id)
      student.delete(currentUser=currentUser)
      response = dict(message = 'Student Deleted')
      status = HTTP_200_OK
    except Student.DoesNotExist:
      response=dict(error = 'Student Not Found')
      status = HTTP_404_NOT_FOUND
    except Student.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Students found"), HTTP_400_BAD_REQUEST
    finally:
      return response, status
