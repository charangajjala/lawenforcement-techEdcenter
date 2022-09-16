from rest_framework.status import *

from meta.models import Address
from .models import User
from .serializers import UserRequest, UserResponse, UserResponse2, UsersList

from django.db.models.query_utils import Q
from django.db.utils import IntegrityError

class UserService():

    @classmethod
    def getAllUsers(cls,params=None):
        print("<---- users.services.UserService.getAllUsers ---->")
        try:
            if params:
                id = params.get('sid')
                email = params.get('semail')
                firstName = params.get('sfname')
                lastName=params.get('slname')
                phone = params.get('sphone')
                isSuperUser = True if params.get('sspuser')=='true' else False if params.get('sspuser')=='false' else None
                isAdmin = True if params.get('sadmin')=='true' else False if params.get('sadmin')=='false' else None

                users = User.objects.all()

                if id:
                    users = users.filter(id=id)
                if firstName:
                    users = users.filter(firstName__icontains=firstName)
                if lastName:
                    users = users.filter(lastName__icontains=lastName)
                if email:
                    users = users.filter(email=email)
                if phone:
                    users = users.filter(phone__contains=phone)
                if isSuperUser in (True,False):
                    users = users.filter(isSuperUser=isSuperUser)
                if isAdmin in (True,False):
                    users = users.filter(isAdmin=isAdmin)
            else:
                users = User.objects.defer('created','createdBy','history','isDeleted')
            
            usersResponse = UserResponse2(users, many=True)
            response,status = usersResponse.data,HTTP_200_OK
            
        except ValueError:
            response, status = dict(error = "Getting a None somewhere"), HTTP_404_NOT_FOUND
        return response, status
    @classmethod
    def getUser(cls, id):
        print("<---- users.services.UserService.getUser ---->")

        try:
            user = User.objects.get(id=id)
            userResponse = UserResponse(user)
            response, status = userResponse.data, HTTP_200_OK
        except User.DoesNotExist:
            response, status = dict(error = "User not found"), HTTP_404_NOT_FOUND
        except User.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Users found"), HTTP_400_BAD_REQUEST

        return response, status

    @classmethod
    def deleteUser(cls, id, currentUser):
        print("<---- users.services.UserService.deleteUser ---->")
        
        try:
            user = User.objects.get(id=id)
            user.delete(currentUser=currentUser)
            response, status = dict(message = "User Deleted"), HTTP_200_OK
        except User.DoesNotExist:
            response, status = dict(error = "User not found"), HTTP_404_NOT_FOUND
        except User.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Users found"), HTTP_400_BAD_REQUEST
            print("Multiple users with one id, WTF!!")

        return response, status

    @classmethod
    def createUser(cls, data, currentUser):
        print("<---- users.services.UserService.createUser ---->")

        userRequest = UserRequest(data=data)
        try:
            if userRequest.is_valid():
                address = userRequest.validated_data.pop('address', None)
                addressObj = Address.objects.create(**address) if address else None
                user = User.objects.create(
                    **dict(
                        userRequest.validated_data,
                        address = addressObj,
                        createdBy = currentUser
                    )
                )
                userResponse = UserResponse(user)
                response, status = userResponse.data, HTTP_201_CREATED
            else:
                print("Data invalid")
                print(userRequest.errors)
                response, status = userRequest.errors, HTTP_400_BAD_REQUEST

        except IntegrityError as e:
            response, status = e.__dict__, HTTP_409_CONFLICT
        
        return response, status

    @classmethod
    def updateUser(cls, id, data, currentUser):
        print("<---- users.services.UserService.updateUser ---->")
        
        userRequest = UserRequest(data=data, partial=True)
        try:
            if userRequest.is_valid():
                validData=userRequest.validated_data
                oldValues = {}
                user = User.objects.get(id = id)
    
                addressObj = validData.pop('address',None)
                for (k, v) in userRequest.validated_data.items():
                    oldValues[k] = getattr(user, k)
                    setattr(user, k, v)
                if addressObj:
                    if user.address:
                        for k, v in addressObj.items():

                            oldValues[k] = getattr(user.address, k)
                            setattr(user.address, k, v)
                    else:
                        newAddress = Address.objects.create(**addressObj)
                        setattr(user,'address',newAddress)

                user.update(oldValues, currentUser)
                userResponse = UserResponse(user)

                response, status = userResponse.data, HTTP_200_OK
            else:
                print("Data invalid")
                print(userRequest.errors)
                response, status = userRequest.errors, HTTP_400_BAD_REQUEST
        
        except User.DoesNotExist:
            response, status = dict(error = "User not found"), HTTP_404_NOT_FOUND
        except User.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Users found"), HTTP_400_BAD_REQUEST
        return response, status

class StandardUserServices:

    @classmethod
    def getUser(cls,currentUser):
        email = currentUser.email
        try:
            print('getting user data')
            user = User.objects.get(email=email)
            userResponse = UserRequest(user)
            response, status = userResponse.data, HTTP_200_OK
        except User.DoesNotExist:
            response, status = dict(error = "User not found"), HTTP_404_NOT_FOUND
        except User.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Users found"), HTTP_400_BAD_REQUEST
            print("Multiple users with one id, WTF!!")

        return response, status

    @classmethod
    def getListofUsers(cls):
        users = User.objects.only('id','firstName','lastName','email','phone')
        userResponse = UsersList(users,many=True)
        response = userResponse.data
        status = HTTP_200_OK
        return response,status

    @classmethod
    def updateUser(cls,data,currentUser):
        userRequest = UserRequest(data=data, partial=True)
        try:
            if userRequest.is_valid():
                print("Data valid")
                oldValues = {}
                user = User.objects.get(email = currentUser.email)
    
                address = userRequest.validated_data.pop('address', None)

                for (k, v) in userRequest.validated_data.items():
                    oldValues[k] = getattr(user, k)
                    setattr(user, k, v)
                
                if address:
                    if user.address:
                        for (k, v) in address.items():
                            oldValues[k] = getattr(user.address, k)
                            setattr(user.address, k, v)
                    else:
                        addressObj = Address.objects.create(**address)
                        user.address = addressObj
                        for (k, v) in address.items():
                            oldValues[k] = None
                            

                user.update(oldValues, currentUser)
                user.save()
                userResponse = UserRequest(user)
                response, status = userResponse.data, HTTP_200_OK
                print(response)
            else:
                print("Data invalid")
                print(userRequest.errors)
                response, status = userRequest.errors, HTTP_400_BAD_REQUEST
        
        except User.DoesNotExist:
            response, status = dict(error = "User not found"), HTTP_404_NOT_FOUND
        except User.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Users found"), HTTP_400_BAD_REQUEST
            print("Multiple users with one id, WTF!!")

        return response, status

    @classmethod
    def createUser(cls, data):

        userRequest = UserRequest(data=data)
        if userRequest.is_valid():
            print("Data valid")
            print(userRequest.validated_data)

            address = userRequest.validated_data.pop('address', None)
            addressObj = Address.objects.create(**address) if address else None
            
            print('User object about to be created')
            user = User.objects.create(
                **dict(
                    userRequest.validated_data,
                    address = addressObj,
                )
            )
            userResponse = UserRequest(user)
            response, status = userResponse.data, HTTP_201_CREATED
            print(response)
        else:
            print("Data invalid")
            print(userRequest.errors)
            response, status = userRequest.errors, HTTP_400_BAD_REQUEST

        return response, status
