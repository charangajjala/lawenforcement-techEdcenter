from rest_framework.status import *

from meta.models import Address
from .models import User
from .serializers import UserRequest, UserResponse, UserResponse2

class UserService():

    @classmethod
    def getAllUsers(cls):
        print("<---- users.services.UserService.getAllUsers ---->")
        
        users = User.objects.defer('created', 'createdBy', 'history', 'isDeleted')
        usersResponse = UserResponse2(users, many=True)
        response = usersResponse.data
        print(response)
        return response, HTTP_200_OK
        
    @classmethod
    def getUser(cls, id):
        print("<---- users.services.UserService.getUser ---->")

        try:
            user = User.objects.get(id=id)
            userResponse = UserResponse(user)
            response, status = userResponse.data, HTTP_200_OK
            print(response)
        except User.DoesNotExist:
            response, status = dict(error = "User not found"), HTTP_404_NOT_FOUND
        except User.MultipleObjectsReturned:
            response, status = dict(error = "Multiple Users found"), HTTP_400_BAD_REQUEST
            print("Multiple users with one id, WTF!!")

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
                    createdBy = currentUser
                )
            )
            userResponse = UserResponse(user)
            print('this is user response', userResponse)
            response, status = userResponse.data, HTTP_201_CREATED
            print(response)
        else:
            print("Data invalid")
            print(userRequest.errors)
            response, status = userRequest.errors, HTTP_400_BAD_REQUEST

        return response, status

    @classmethod
    def updateUser(cls, id, data, currentUser):
        print("<---- users.services.UserService.updateUser ---->")
        
        userRequest = UserRequest(data=data, partial=True)
        try:
            if userRequest.is_valid():
                print("Data valid")
                print(userRequest.validated_data)
                oldValues = {}
                user = User.objects.get(id = id)
    
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
                
                userResponse = UserResponse(user)
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
