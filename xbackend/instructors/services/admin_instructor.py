from instructors.serializers import InstructorRequest, InstructorResponse, UserListResponse
from instructors.models import Instructor
from meta.models import File,Address,Contact,Note
from users.models import User

from django.db.models.query_utils import Q
from django.db.utils import IntegrityError

from rest_framework.status import *


class AdminInstructorService:
   
    @classmethod
    def getAllInstructors(cls,params=None):
        global users
        users=None
        try:
            if params:
                id = params.get('sid')
                firstName = params.get('sfname')
                lastName = params.get('slname')
                phone = params.get('sphone')
                email=params.get('semail')
                isActive = True if params.get('sactive')=='true' else False if params.get('sactive')=='false' else None
                instructors = Instructor.objects.all()
                if firstName or email or lastName:
                    users = User.objects.all()
                    if firstName:
                        instructors = instructors.filter(firstName__startswith=firstName)
                    if lastName:
                        instructors = instructors.filter(lastName__startswith=lastName)
                    if email:
                        instructors = instructors.filter(email=email)
                    if phone:
                        instructors = instructors.filter(phone__contains=phone)                   

                if id:
                    instructors = instructors.filter(id=id)
                if isActive in (True,False):
                    instructors = instructors.filter(isActive=isActive)

            else:
                instructors = Instructor.objects.only('user')
            instructorsResponse = UserListResponse(instructors,many=True)
            response,status = instructorsResponse.data,HTTP_200_OK   
        except ValueError:
            response,status = dict(error = "There is some error that i dont know"),HTTP_404_NOT_FOUND
        return response, status

    @classmethod
    def createInstructor(cls,data,currentUser):
        instructorRequest = InstructorRequest(data=data)
        try:        
            if instructorRequest.is_valid():
                print("data is valid")
                validData = instructorRequest.validated_data
                imageid = validData.pop('image')
                fileObj = File.objects.get(id=imageid)

                userId = validData.pop('userId',None)
                userobj = User.objects.get(id=userId) if userId else None
                
                agencyAddress = validData.pop('agencyAddress',None)
                agencyAddressObj = Address.objects.create(**agencyAddress) if agencyAddress else None

                agencyContact = validData.pop('agencyContact',None)
                agencyContactObj = Contact.objects.create(**agencyContact) if agencyContact else None

                emergencyContact = validData.pop('emergencyContact',None)
                emergencyContactObj = Contact.objects.create(**emergencyContact) if emergencyContact else None
                
                docs = validData.pop('docs',None)
                adminNotes = validData.pop('adminNotes',None)
                instructor = Instructor.objects.create(
                    **dict(
                        validData,
                        user = userobj,
                        image=fileObj,
                        agencyAddress=agencyAddressObj,
                        agencyContact = agencyContactObj,
                        emergencyContact = emergencyContactObj,
                        createdBy = currentUser
                    )
                )
                if docs:
                    instructor.docs.add(*File.objects.filter(id__in=[doc.get('id') for doc in docs]))
                if adminNotes:
                    for note in adminNotes:
                        instructor.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=currentUser)))
                
                instructorResponse = InstructorResponse(instructor)
                print(instructorResponse.data)     
                
                response,status = instructorResponse.data,HTTP_200_OK
                print('Instructor response printed')
            else:
                print('data is invalid')
                print(instructorRequest.errors)
                response = instructorRequest.errors
                status = HTTP_400_BAD_REQUEST

        except IntegrityError:
            response = dict(error = "Requested User was already a instructor")
            status = HTTP_400_BAD_REQUEST

        return response,status
            


    @classmethod
    def updateInstructor(cls,id,data,currentUser):
        instructorRequest = InstructorRequest(data=data,partial=True)
        try:
            if instructorRequest.is_valid():
                print('Data is valid',instructorRequest.validated_data)
                oldValues = {}

                validData = instructorRequest.validated_data
                instructor = Instructor.objects.get(id = id)

                userId = validData.pop('userId',None)
                userobj = User.objects.get(id=userId) if userId else None

                agencyAddress = validData.pop('agencyAddress',None)
                agencyContact = validData.pop('agencyContact',None)
                emergencyContact = validData.pop('emergencyContact',None)
                docs = validData.pop('docs',None)
                adminNotes = validData.pop('adminNotes',None)

                for (k, v) in validData.items():
                    oldValues[k] =  getattr(instructor, k)
                    setattr(instructor, k, v)

                if userobj:
                    if instructor.user:
                        instructor.user = userobj

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
                    for note in adminNotes:
                        instructor.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=currentUser)))
                
                instructor.update(oldValues,currentUser)
                instructorResponse = InstructorResponse(instructor)
                response = instructorResponse.data
                status = HTTP_200_OK

                return response,status
            else:
                print("Data invalid")
                print(instructorRequest.errors)
                response, status = instructorRequest.errors, HTTP_400_BAD_REQUEST

        except Instructor.DoesNotExist:
            response, status = dict(error = "Instructor not found"), HTTP_404_NOT_FOUND

        except Instructor.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Instructors found"), HTTP_400_BAD_REQUEST
            print("Multiple Instructors with one id, WTF!!")

        return response, status


    @classmethod
    def getInstructor(cls,id):
        try:
            instructor = Instructor.objects.get(id=id)
            instructorResponse = InstructorResponse(instructor)
            response,status = instructorResponse.data,HTTP_200_OK

        except Instructor.DoesNotExist:
            response, status = dict(error = "Instructor not found"), HTTP_404_NOT_FOUND

        except Instructor.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Instructors found"), HTTP_400_BAD_REQUEST
            print("Multiple Instructors with one id, WTF!!")

        return response, status


    @classmethod
    def deleteInstructor(cls,id,currentUser):
        try:
            instructor = Instructor.objects.get(id=id)
            #add additional if required
            instructor.delete(currentUser=currentUser)
            response,status = dict(message = "Instructor Deleted"),HTTP_200_OK

        except Instructor.DoesNotExist:
            response, status = dict(error = "Instructor not found"), HTTP_404_NOT_FOUND

        except Instructor.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Instructors found"), HTTP_400_BAD_REQUEST
            print("Multiple Instructors with one id, WTF!!")

        return response, status