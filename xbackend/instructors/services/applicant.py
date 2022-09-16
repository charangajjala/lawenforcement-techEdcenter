from functools import partial
from rest_framework.status import *
from instructors.models import *
from instructors.serializers import *
from users.models import *

class InstructorApplicantServices:

  @classmethod
  def createApplicant(cls,data):
    applicantRequest = ApplicantRequest(data=data)
    if applicantRequest.is_valid():
      validData = applicantRequest.data
      print(validData)

      userId = validData.pop('userId',None)
      coursePreferences = validData.pop('coursePreferences',None)
      docs = validData.pop('docs',None)
      comments = validData.pop('comments',None)

      # if email:
      #   try:
      #     newUser = User.objects.get(email=email)
      #   except User.DoesNotExist:
      #     newUser = User.objects.create(
      #       **dict(
      #         validData,
      #         email=email
      #       )
      #     )

      userObj = User.objects.get(id=userId) 

      applicant = Applicant.objects.create(
        **dict(
          user = userObj,
          comments = comments,
        )
      )

      if coursePreferences:
        applicant.coursePreferences.add(*Course.objects.filter(id__in=[course.get('id') for course in coursePreferences]))

      if docs:
        applicant.docs.add(*File.objects.filter(id__in=[doc.get('id') for doc in docs]))

      # if adminNotes:
      #   applicant.adminNotes.add(*Note.objects.filter(id__in=[note.get('id') for note in adminNotes]))

      status = HTTP_201_CREATED
      response = dict(success = 'Applicant Created')
      return response,status
    else:
      print("Data invalid")
      print(ApplicantRequest.errors)
      response, status = ApplicantRequest.errors, HTTP_400_BAD_REQUEST
      
  @classmethod
  def updateApplicant(cls,user,data):
    applicantRequest = ApplicantRequest(data=data,partial=True)
    if applicantRequest.is_valid():
      print('Data is valid')
      print(applicantRequest.validated_data)
      oldValues={}
      validData = applicantRequest.validated_data
      applicant = Applicant.objects.get(user=user)
      coursePreferences = validData.pop('coursePreferences',None)
      docs = validData.pop('docs',None)
      adminNotes = validData.pop('adminNotes',None)

      for (k, v) in validData.items():
          oldValues[k] =  getattr(applicant, k)
          setattr(applicant, k, v)

      if coursePreferences:
          if applicant.coursePreferences:
              for (k,v) in coursePreferences.items():
                  oldValues[k] = getattr(applicant.coursePreferences,k)
                  setattr(applicant.coursePreferences, k,v)
      
      if docs:
          for doc in docs:
              docObj = File.objects.get(id=doc.get('id'))
              if doc.get('action') == 'ADD':
                  applicant.docs.add(docObj)
              if doc.get('action') == 'REMOVE':
                  applicant.docs.remove(docObj)
      
      if adminNotes:
          for note in adminNotes:
              noteObj = Note.objects.get(id=doc.get('id'))
              if note.get('action') == 'ADD':
                  applicant.adminNotes.add(noteObj)
              if note.get('action') == 'REMOVE':
                  applicant.adminNotes.remove(noteObj)

      applicant.update(oldValues)
      applicantResponse = ApplicantResponse(applicant)
      response,status = applicantResponse.data,HTTP_200_OK
      return response,status

    else:
        print("Data invalid")
        print(applicantRequest.errors)
        response, status = applicantRequest.errors, HTTP_400_BAD_REQUEST


  @classmethod
  def getApplicant(cls,user):
    print(user)
    try:
      applicant = Applicant.objects.get(user=user)
      application = ApplicantResponse(applicant)
      response = application.data
      status = HTTP_200_OK

    except Applicant.DoesNotExist:
      response, status = dict(error = "Applicant not found"), HTTP_404_NOT_FOUND

    except Applicant.MultipleObjectsReturned:
      response, status = dict(error = "Multiple applicants found"), HTTP_400_BAD_REQUEST
      print("Multiple Applicants WTF!!")
      
    return response, status