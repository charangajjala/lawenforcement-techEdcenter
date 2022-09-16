from django.http import response
from hosts.models import Location
from hosts.serializers import *
from meta.models import Address,Contact,Note

from rest_framework.status import *

from django.db.utils import IntegrityError

class StandardLocationServices:
  @classmethod
  def createLocation(cls,data):
    locationRequest = LocationRequest(data=data)
    try:
      if locationRequest.is_valid():
        print('Location Data is Valid')
        validData = locationRequest.validated_data

        address = validData.pop('address',None)
        addressObj = Address.objects.create(**address) if address else None

        contact = validData.pop('locationContact',None)
        contactObj = Contact.objects.create(**contact) if contact else None

        adminNotes = validData.pop('adminNotes',None)
        intel = validData.pop('intel',None)
        location = Location.objects.create(
          **dict(
            validData,
            address = addressObj,
            locationContact = contactObj
          )
        )
        if adminNotes:
          for note in adminNotes:
              location.adminNotes.add(Note.objects.create(**dict(text=note)))

        if intel:
          for note in intel:
              location.intel.add(Note.objects.create(**dict(text=note)))


        locationResponse = LocationResponse(location)
        response = locationResponse.data
        status = HTTP_201_CREATED

      else:
        print('Location Data is Invalid')
        response = locationRequest.errors
        status = HTTP_400_BAD_REQUEST
    except IntegrityError:
      response = dict(error = 'Request location is already there')
      status = HTTP_409_CONFLICT

    return response,status      
      
  @classmethod
  def updateLocation(cls,data,user,id):
    locationRequest = LocationRequest(data=data,partial=True)
    try:
      if locationRequest.is_valid():
        print('Location updation details are valid')
        validData = locationRequest.validated_data
        oldValues = {}

        #to verfy if he is a host
        Host.objects.get(contactUser=user)
        location = Location.objects.get(id=id)
        
        address = validData.pop('address',None)
        contact = validData.pop('locationContact',None)

        for (k, v) in validData.items():
          oldValues[k] =  getattr(location, k)
          setattr(location, k, v)

        if address:
            if location.address:
                for (k, v) in address.items():
                    oldValues[k] = getattr(location.address, k)
                    setattr(location.address, k, v)
            else:
                addressObj = Address.objects.create(**address)
                location.address = addressObj
                for (k, v) in address.items():
                    oldValues[k] = None
        if contact:
          if location.contact:
              for (k, v) in contact.items():
                  oldValues[k] = getattr(location.contact, k)
                  setattr(location.contact, k, v)
          else:
              contactObj = Contact.objects.create(**address)
              location.contact = contactObj
              for (k, v) in contact.items():
                  oldValues[k] = None     

        location.update(oldValues,currentUser=user)
        locationResponse = LocationResponse(location)
        response,status = locationResponse.data,HTTP_200_OK
      else:
        print('Location Updata request Invalid')
        response,status = locationRequest.errors,HTTP_400_BAD_REQUEST
    except Host.DoesNotExist:
        response, status = dict(error = "You are not a host you cant access Locations"), HTTP_400_BAD_REQUEST
    except Host.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Hosts found"), HTTP_400_BAD_REQUEST
    except Location.DoesNotExist:
        response,status = dict(error = 'Requested Location not found'),HTTP_400_BAD_REQUEST
    except Location.MultipleObjectsReturned:
        response,status = dict(error = 'Multiple location Objects found for the same Id'),HTTP_400_BAD_REQUEST
    return response,status


  @classmethod
  def getLocations(cls):
    location =Location.objects.all()
    locationResponse = LocationResponse(location,many=True)
    response,status = locationResponse.data,HTTP_200_OK
    return response,status

  @classmethod
  def getLocation(cls,id):
    location=Location.objects.get(id=id)
    locationResponse = LocationResponse(location)
    response,status=locationResponse.data,HTTP_200_OK
    return response,status