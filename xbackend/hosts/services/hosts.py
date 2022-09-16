from hosts.serializers.hosts import StandardHostResponse,StandardHostRequest,HostListResponse
from hosts.models import *

from rest_framework.status import *

class StandardHostServices:
  @classmethod
  def hostProfile(cls,user):
    try:
      hostObjs = Host.objects.get(contactUser=user)
      hosts = StandardHostResponse(hostObjs)
      response = hosts.data
      status = HTTP_200_OK
    except Host.DoesNotExist:
      response, status = dict(error = "Host not found"), HTTP_404_NOT_FOUND
    except Host.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Hosts found"), HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def getList(cls):
    hostObjs = Host.objects.all()
    hostsResponse = HostListResponse(hostObjs,many=True)
    response,status = hostsResponse.data,HTTP_200_OK
    return response,status

  @classmethod
  def getprofile(cls,id):
    try:
      host = Host.objects.get(id=id)
      profile=StandardHostResponse(host)
      response,status=profile.data,HTTP_200_OK
    except Host.DoesNotExist:
      response, status = dict(error = "Host not found"), HTTP_404_NOT_FOUND
    except Host.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Hosts found"), HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def updateProfile(cls,data,currentUser):
    hostRequest = StandardHostRequest(data=data,partial=True)
    try:
      if hostRequest.is_valid():
        print('Host Data is Valid',hostRequest.validated_data)
        validData = hostRequest.validated_data
        oldValues = {}
        host = Host.objects.get(contactUser=currentUser)
        address = validData.pop('address',None)
        supervisorContact = validData.pop('supervisorContact',None)

        logoId = validData.pop('logo',None)
        logoObj = File.objects.get(id=logoId) if logoId else None

        if logoObj:
          setattr(host,'logo',logoObj)

        courses = validData.pop('courses',None)
        locations = validData.pop('locations',None)
        docs = validData.pop('docs',None)

        for (k, v) in validData.items():
          oldValues[k] =  getattr(host, k)
          setattr(host, k, v)
        if address:
          if host.address:
              for (k,v) in address.items():
                  oldValues[k] = getattr(host.address,k)
                  setattr(host.address, k,v)
        
        if supervisorContact:
          if host.supervisorContact:
              for (k,v) in supervisorContact.items():
                  oldValues[k] = getattr(host.supervisorContact,k)
                  setattr(host.supervisorContact, k,v)
        
        if docs:
            for doc in docs:
                docObj = File.objects.get(id=doc.get('id'))
                if doc.get('action') == 'ADD':
                    host.docs.add(docObj)
                if doc.get('action') == 'REMOVE':
                    host.docs.remove(docObj)

        if locations:
            for location in locations:
                locationObj = Location.objects.get(id=location.get('id'))
                if location.get('action') == 'ADD':
                    host.locations.add(locationObj)
                if location.get('action') == 'REMOVE':
                    host.locations.remove(locationObj)

        if courses:
          for course in courses:
            courseObj = Course.objects.get(id =course.get('id'))
            if course.get('action') == 'ADD':
              host.courses.add(courseObj)
            if course.get('action') == 'REMOVE':
              host.courses.remove(courseObj)

        host.update(oldValues,currentUser)
        hostResponse = StandardHostResponse(host)
        response = hostResponse.data
        status = HTTP_200_OK
      else:
        print("Host Data invalid")
        print(hostRequest.errors)
        response, status = hostRequest.errors, HTTP_400_BAD_REQUEST


    except Host.DoesNotExist:
            response, status = dict(error = "Host Profile not found"), HTTP_404_NOT_FOUND

    return response, status   

  @classmethod
  def createHost(cls,user,data):
    hostRequest = StandardHostRequest(data=data)
    if hostRequest.is_valid():
      print('Host Data is Valid',hostRequest.validated_data)
      validData = hostRequest.validated_data

      address = validData.pop('address',None)
      addressObj = Address.objects.create(**address) if address else None
      supervisorContact = validData.pop('supervisorContact',None)
      supervisorContactObj = Contact.objects.create(**supervisorContact) if supervisorContact else None

      logoId = validData.pop('logo',None)
      logoObj = File.objects.get(id=logoId)

      courses = validData.pop('courses',None)
      locations = validData.pop('locations',None)
      docs = validData.pop('docs',None)
      
      host = Host.objects.create(
        **dict(
          validData,
          contactUser = user,
          logo=logoObj,
          address = addressObj,
          supervisorContact = supervisorContactObj,
          createdBy = user
        )
      )
      print('Host Genarated')

      if courses:
        for course in courses:
          courseObj = Course.objects.get(id=course.get('id'))
          if course.get('action') == 'ADD':
            host.docs.add(courseObj)
          if course.get('action') == 'DELETE':
            host.docs.remove(courseObj)

      if locations:
        for location in locations:
          locationObj = Location.objects.get(id=location.get('id'))
          if location.get('action') == 'ADD':
            host.docs.add(locationObj)
          if location.get('action') == 'DELETE':
            host.docs.remove(locationObj)

      if docs:
        for doc in docs:
            docObj = File.objects.get(id=doc.get('id'))
            if doc.get('action') == 'ADD':
                host.docs.add(docObj)
            if doc.get('action') == 'REMOVE':
                host.docs.remove(docObj)

      hostResponse = StandardHostResponse(host)
      response = hostResponse.data
      status  = HTTP_201_CREATED
    else:
      print('Host data Invalid',hostRequest.errors)
      response = hostRequest.errors
      status = HTTP_400_BAD_REQUEST
    return response,status

