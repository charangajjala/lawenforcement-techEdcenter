from rest_framework.status import HTTP_200_OK
from instructors.serializers import *
from instructors.models import *

from rest_framework.status import * 

class InstructorService:

  @classmethod
  def getInstructorProfile(cls,user):
    try:
      instructor = Instructor.objects.get(user=user)
      profile = InstructorProfile(instructor)
      response = profile.data
      status = HTTP_200_OK

    except Instructor.DoesNotExist:
      response, status = dict(error = "Instructor not found"), HTTP_404_NOT_FOUND

    except Instructor.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Instructors found"), HTTP_400_BAD_REQUEST
      print("Multiple Instructors with one id, WTF!!")
      
    return response, status

  @classmethod
  def getInstructor(cls,id):
    try:
      instructorObj = Instructor.objects.get(id=id)
      profile=InstructorProfile(instructorObj)
      response,status = profile.data,HTTP_200_OK
    except Instructor.DoesNotExist:
      response, status = dict(error = "Instructor not found"), HTTP_404_NOT_FOUND
    except Instructor.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Instructors found"), HTTP_400_BAD_REQUEST
    return response, status

  @classmethod
  def getInstructorList(cls):
    instructors = Instructor.objects.only('id','image','bio','user')
    instructorList = InstructorlistResponse(instructors,many=True)
    response = instructorList.data
    status =HTTP_200_OK
    return response,status

  @classmethod
  def updateProfile(cls,user,data):
    instructorRequest = InstructorProfile(data=data,partial=True)
    try:
      if instructorRequest.is_valid():
          print('Data is valid',instructorRequest.validated_data)
          oldValues = {}

          validData = instructorRequest.validated_data
          print('Validated data is copied')
          instructor = Instructor.objects.get(user =user)
          print('instructor object fetched correct')
          agencyAddress = validData.pop('agencyAddress',None)
          agencyContact = validData.pop('agencyContact',None)
          emergencyContact = validData.pop('emergencyContact',None)
          docs = validData.pop('docs',None)
          adminNotes = validData.pop('adminNotes',None)

          for (k, v) in validData.items():
              oldValues[k] =  getattr(instructor, k)
              setattr(instructor, k, v)

          if agencyAddress:
              if instructor.agencyAddress:
                  for (k,v) in agencyAddress.items():
                      oldValues[k] = getattr(instructor.agencyAddress,k)
                      setattr(instructor.agencyAddress, k,v)
                      
          if agencyContact:
              if instructor.agencyContact:
                  for (k,v) in agencyContact.items():
                      oldValues[k] = getattr(instructor.agencyContact,k)
                      setattr(instructor.agencyContact, k,v)

          if emergencyContact:
              if instructor.emergencyContact:
                  for (k,v) in emergencyContact.items():
                      oldValues[k] = getattr(instructor.emergencyContact,k)
                      setattr(instructor.emergencyContact, k,v)

          if docs:
              for doc in docs:
                  docObj = File.objects.get(id=doc.get('id'))
                  if doc.get('action') == 'ADD':
                      instructor.docs.add(docObj)
                  if doc.get('action') == 'REMOVE':
                      instructor.docs.remove(docObj)
          
          if adminNotes:
            instructor.adminNotes.add(*Note.objects.filter(id__in=[note.get('id') for note in adminNotes]))
          
          print('all the updates are done about to')
          instructor.update(oldValues)
          print('About to genarate response')
          instructorResponse = InstructorProfile(instructor)
          print('response genarated')
          response = instructorResponse.data
          print(response)
          status = HTTP_200_OK

          return response,status
      else:
          print("Data invalid")
          print(instructorRequest.errors)
          response, status = instructorRequest.errors, HTTP_400_BAD_REQUEST          

    except Instructor.DoesNotExist:
        response, status = dict(error = "Instructor Profile not found"), HTTP_404_NOT_FOUND

    except Instructor.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Instructors found"), HTTP_400_BAD_REQUEST
        print("Multiple Instructors with one id, WTF!!")

    return response, status