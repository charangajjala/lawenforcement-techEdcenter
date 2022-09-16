from hosts.serializers import *
from hosts.models import *

from rest_framework.status import *
from django.db.models.query_utils import Q

from datetime import *

class AdminLocationsSerivices:
  @classmethod
  def createLocation(cls,data,currentUser):
    locationRequest = AdminLocationRequest(data=data,partial=True)
    if locationRequest.is_valid():
      print('Location data is valid')
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
          locationContact = contactObj,
          createdBy = currentUser
        )
      )

      if adminNotes:
          for note in adminNotes:
            location.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=currentUser)))
      
      if intel:
          for note in intel:
            print(note)
            location.intel.add(Note.objects.create(**dict(text=note, createdBy=currentUser)))

      locationResponse = AdminLocationResponse(location)
      response = locationResponse.data
      status = HTTP_201_CREATED
      
    else:
      print('Location Data is Invalid')
      response = locationRequest.errors
      status = HTTP_400_BAD_REQUEST
    return response,status


  @classmethod
  def getAllLocations(cls,params=None):
    global createdon,addresses
    createdon,addresses=None,None
    try:
      if params:
        id = params.get('sid')
        city = params.get('scity')
        name = params.get('name')
        seats = params.get('sseats')
        state = params.get('sstate')
        isActive = True if params.get('sactive')=='true' else False if params.get('sactive')=='false' else None

        created = params.get('screatedat')

        if created:
            createdon = datetime.strptime(created,'%Y-%m-%d')

        if city or state:
          addresses = Address.objects.all()
          if city:
            addresses = addresses.filter(city__startswith=city)
          if state:
            addresses = addresses.filter(state__exact=state)

        locations = Location.objects.all()
        if id:
          locations = locations.filter(id=id)
        if name:
          locations = locations.filter(name__startswith=name)
        if seats:
          locations = locations.filter(seats__exact=seats)
        if addresses:
          locations = locations.filter(address__in=addresses)
        if isActive in (True,False):
          locations = locations.filter(isActive=isActive)
        if created:
          locations = locations.filter(created__date=createdon)

      else:
        locations = Location.objects.all()    
      locationlist = AdminLocationsListResponse(locations,many=True)
      response = locationlist.data
      status = HTTP_200_OK
    except ValueError:
      response,status = dict(error = "There is some error that i dont know"), HTTP_404_NOT_FOUND

    return response,status

class AdminLocationServices:
  @classmethod
  def getLocation(cls,id):
    try:
      location = Location.objects.get(id=id)
      locationReponse = AdminLocationResponse(location)
      response = locationReponse.data
      status = HTTP_200_OK
    except Location.DoesNotExist:
      response, status = dict(error = "Location not found"), HTTP_404_NOT_FOUND
    except Location.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Locations found"), HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def updateLocation(cls,data,currentUser,id):
    locationRequest = AdminLocationRequest(data=data,partial=True)
    try:
      if locationRequest.is_valid():
        print('Location data is valid',locationRequest.validated_data)
        validData = locationRequest.validated_data
        oldValues = {}

        location = Location.objects.get(id=id)

        address = validData.pop('address',None)
        contact = validData.pop('contact',None)

        adminNotes = validData.pop('adminNotes',None)
        intel = validData.pop('intel',None)

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
          if location.locationContact:
              for (k, v) in contact.items():
                  oldValues[k] = getattr(location.contact, k)
                  setattr(location.contact, k, v)
          else:
              contactObj = Contact.objects.create(**address)
              location.locationContact = contactObj
              for (k, v) in contact.items():
                  oldValues[k] = None        

        if adminNotes:
          for note in adminNotes:
            location.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=currentUser)))
        
        if intel:
          for note in intel:
            location.intel.add(Note.objects.create(**dict(note)))

        location.update(oldValues)
        locationResponse = AdminLocationResponse(location)
        print(locationResponse.data)
        response = locationResponse.data
        status = HTTP_200_OK
      else:
        print('Location Data is Invalid',locationRequest.errors)
        response = locationRequest.errors
        status = HTTP_400_BAD_REQUEST
    except Location.DoesNotExist:
            response, status = dict(error = "applicant not found"), HTTP_404_NOT_FOUND

    except Location.MultipleObjectsReturned:
        response, status = dict(error = "Multiple applicants found"), HTTP_400_BAD_REQUEST
        print("Multiple applicants with one id, WTF!!")
    return response,status

  @classmethod
  def deleteLocation(cls,id,currentUser):
    try:
      location = Location.objects.get(id=id)
      location.delete(currentUser=currentUser)
      response = dict(message = "Location Deleted")
      status = HTTP_200_OK
    except Location.DoesNotExist:
        response, status = dict(error = "Location not found"), HTTP_404_NOT_FOUND

    except Location.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Locations found"), HTTP_400_BAD_REQUEST
        print("Multiple Locations with one id, WTF!!")

    return response, status