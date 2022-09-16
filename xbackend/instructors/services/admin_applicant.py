from instructors.serializers import *
from instructors.models import *

from rest_framework.status import *

from django.db.models.query_utils import Q

class AdminApplicantsService:

    @classmethod
    def getAllApplicants(cls,params=None):
        global users
        users = None
        try:
            if params:
                id = params.get('sid')
                firstName = params.get('sfname')
                lastName = params.get('slname')
                email = params.get('semail')
                phone = params.get('sphone')
                status = params.get('sactive')

                for v in Applicant.Status:
                    if status==v._name_:
                        statusNo = v._value_

                if firstName or email or lastName:
                    users = User.objects.all()
                    if firstName:
                        users = users.filter(firstName__startswith=firstName)
                    if lastName:
                        users = users.filter(lastName__startswith=lastName)
                    if email:
                        users = users.filter(email=email)
                    if phone:
                        users = users.filter(phone__contains =phone)

                applicants = Applicant.objects.all()
                if id:
                    applicants =applicants.filter(id=id)
                if status:
                    applicants=applicants.filter(status=statusNo)
                if users:
                    applicants=applicants.filter(user_in=users)
            else:
                applicants=Applicant.objects.all()

            applicantsResponse = ApplicantListResponse(applicants,many=True)      
            response,status = applicantsResponse.data,HTTP_200_OK  
        except ValueError:
            response,status = dict(error = "There is some error that i dont know"),HTTP_404_NOT_FOUND
        return response, status

    @classmethod
    def getApplicant(cls,id):
        try:
            applicant = Applicant.objects.get(id=id)
            applicantResponse = ApplicantResponse(applicant)
            response,status = applicantResponse.data,HTTP_200_OK

        except Applicant.DoesNotExist:
            response, status = dict(error = "Applicant not found"), HTTP_404_NOT_FOUND

        except Applicant.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Applicants found"), HTTP_400_BAD_REQUEST
            print("Multiple Instructors with one id, WTF!!")

        return response, status

    @classmethod
    def updateApplicant(cls,id,data,currentUser):
        applicantRequest = ApplicantRequest(data=data,partial=True)
        try:
            if applicantRequest.is_valid():
                print('Data is Valid')
                print(applicantRequest.validated_data)
                oldValues = {}

                validData = applicantRequest.validated_data
                applicant = Applicant.objects.get(id=id)

                coursePreferences = validData.pop('coursePreferences',None)
                docs = validData.pop('docs',None)
                adminNotes = validData.pop('adminNotes',None)
                print('all The data is popped')

                for (k, v) in validData.items():
                    oldValues[k] =  getattr(applicant, k)
                    setattr(applicant, k, v)

                print('BAsic Updations are Done')

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
                print('Other updations are also done')
                print(oldValues)

                applicant.update(oldValues)
                print('applicant details updated')
                applicantResponse = ApplicantResponse(applicant)
                response,status = applicantResponse.data,HTTP_200_OK
                return response,status

            else:
                print("Data invalid")
                print(applicantRequest.errors)
                response, status = applicantRequest.errors, HTTP_400_BAD_REQUEST

        except Applicant.DoesNotExist:
            response, status = dict(error = "applicant not found"), HTTP_404_NOT_FOUND

        except Applicant.MultipleObjectsReturned:
            response, status = dict(error = "Multiple applicants found"), HTTP_400_BAD_REQUEST
            print("Multiple applicants with one id, WTF!!")

        return response, status

    @classmethod
    def deleteApplicant(cls,id,currentUser):
        try:
            applicant = Applicant.objects.get(id=id)
            #add additional if required
            applicant.delete(currentUser=currentUser)
            response,status = dict(message = "Applicant Deleted"),HTTP_200_OK

        except Applicant.DoesNotExist:
            response, status = dict(error = "Applicant not found"), HTTP_404_NOT_FOUND

        except Applicant.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Applicants found"), HTTP_400_BAD_REQUEST
            print("Multiple Applicants with one id, WTF!!")

        return response, status
