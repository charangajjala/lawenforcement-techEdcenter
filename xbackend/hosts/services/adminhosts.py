from django.core.exceptions import EmptyResultSet, FieldError
from rest_framework.status import *

from django.db.models.query_utils import *

from datetime import *

from hosts.serializers import *
from hosts.models import *
from meta.models import *
from users.models import *
from courses.models import Course

class AdminHostsServices:

  @classmethod
  def createHost(cls,data,currentUser):
    hostRequest = AdminHostRequest(data=data,partial=True)
    if hostRequest.is_valid():
      print('Host Data is valid',hostRequest.validated_data)
      validData = hostRequest.validated_data

      userId = validData.pop('contactUser',None)
      user = User.objects.get(id=userId)

      address = validData.pop('address',None)
      addressObj = Address.objects.create(**address) if address else None

      supervisorContact = validData.pop('supervisorContact',None)
      supervisorContactObj = Contact.objects.create(**supervisorContact) if supervisorContact else None

      logoId = validData.pop('logo',None)

      courses = validData.pop('courses',None)
      places = validData.pop('locations',None)
      docs = validData.pop('docs',None)
      adminNotes = validData.pop('adminNotes',None)
      if logoId:
        logoObj = File.objects.get(id=logoId)
        host = Host.objects.create(
          **dict(
            validData,
            contactUser = user,
            address = addressObj,
            logo=logoObj,
            supervisorContact = supervisorContactObj,
            createdBy = currentUser
          )
        )
      else:
        host = Host.objects.create(
          **dict(
            validData,
            contactUser = user,
            address = addressObj,
            supervisorContact = supervisorContactObj,
            createdBy = currentUser
          )
        )
      print('Host Genarated')

      if courses:
        host.courses.add(*Course.objects.filter(id__in=[c.get('id') for c in courses]))
      print('courses updated')

      if places:
        host.locations.add(*Location.objects.filter(id__in=[l.get('id') for l in places]))
      print('places updated')

      if docs:
        host.docs.add(*File.objects.filter(id__in=[doc.get('id') for doc in docs]))
      print('docs updated')

      if adminNotes:
        for note in adminNotes:
            host.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=currentUser)))
      print('Admin Notes updated')
      
      hostResponse = AdminHostResponse(host)
      response = hostResponse.data
      status  = HTTP_201_CREATED
    else:
      print('Host data Invalid',hostRequest.errors)
      response = hostRequest.errors
      status = HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def getAllHosts(cls,params=None):
    global createdon,addresses
    createdon = None
    addresses = None
    try:
      if params:
        city = params.get('scity')
        created = params.get('screatedat')
        id=params.get('sid')
        name=params.get('sname')
        state = params.get('sstate')
        status = params.get('sstatus')
        isActive = True if params.get('sactive')=='true' else False if params.get('sactive')=='false' else None
        print('This is status ',status)

        if created:
          createdon = datetime.strptime(created,'%Y-%m-%d')

        if city or state:
          addresses = Address.objects.all()
          if city:
            addresses = addresses.filter(city__startswith=city)
          if state:
            addresses = addresses.filter(state__exact=state)

        hosts = Host.objects.all()
        if id:
          hosts=hosts.filter(id=id)
        if name:
          hosts = hosts.filter(name=name)
        if addresses:
          hosts = hosts.filter(address__in=addresses)
        if isActive in (True,False):
          hosts = hosts.filter(isActive__exact=isActive)
        if status:
          for v in Host.Status:
            if status==v._name_:
              statusNo = v._value_
          hosts = hosts.filter(status=statusNo)
        if created:
          hosts = hosts.filter(created__date=createdon)
      else:
        hosts = Host.objects.all()
      hostList = HostsListResponse(hosts,many=True)
      response = hostList.data
      status = HTTP_200_OK
    except ValueError:
      response,status = dict(message='Requested query does not exist'),HTTP_400_BAD_REQUEST

    return response,status

class AdminHostServices:

  @classmethod
  def getHost(cls,id):
    try:
      host=Host.objects.get(id=id)
      hostResponse = AdminHostResponse(host)
      response= hostResponse.data
      status = HTTP_200_OK
    except Host.DoesNotExist:
      response, status = dict(error = "Host not found"), HTTP_404_NOT_FOUND
    except Host.MultipleObjectsReturned:
      response, status = dict(error = "Multiple Hosts found"), HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def updateHost(cls,id,data,currentUser=None):
    hostRequest = AdminHostRequest(data=data,partial=True)
    try:
      if hostRequest.is_valid():
        print('Host Data is Valid',hostRequest.validated_data)
        validData = hostRequest.validated_data
        oldValues = {}

        host = Host.objects.get(id=id)

        address = validData.pop('address',None)
        supervisorContact = validData.pop('supervisorContact',None)
        logoId = validData.pop('logo',None)          
        courses = validData.pop('courses',None)
        locations = validData.pop('locations',None)
        docs = validData.pop('docs',None)
        adminNotes = validData.pop('adminNotes',None)

        print('before update',host.address.state,host.status)
        for (k, v) in validData.items():
          oldValues[k] =  getattr(host, k)
          print('These are set in the loop',k,v)
          setattr(host, k, v)
        
        if currentUser:
          setattr(host,'createdBy',currentUser)

        if address:
          if host.address:
            for (k,v) in address.items():
                oldValues[k] = getattr(host.address,k)
                setattr(host.address, k,v)

        if logoId:
          logoObj = File.objects.get(id=logoId)

          if host.logo:
            for (k, v) in logoObj.items():
              oldValues[k] = getattr(host.logo, k)
              setattr(host.logo, k,v)

        if supervisorContact:
          if host.supervisorContact:
              for (k,v) in supervisorContact.items():
                  oldValues[k] = getattr(host.supervisorContact,k)
                  setattr(host.supervisorContact, k,v)
        
        if docs:
          host.docs.add(*File.objects.filter(id__in=[doc.get('id') for doc in docs]))
        print('docs updated')          

        if adminNotes:
          for note in adminNotes:
              host.adminNotes.add(Note.objects.create(**dict(text=note, createdBy=currentUser)))
        print('Admin Notes updated')

        if locations:
            for location in locations:
                locationObj = Location.objects.get(id=location.get('id'))
                if location.get('action') == 'ADD':
                    host.locations.add(locationObj)
                if location.get('action') == 'REMOVE':
                    host.locations.remove(locationObj)

        if courses:
          host.courses.add(*Course.objects.filter(id__in=[c.get('id') for c in courses]))
        print('courses updated')
        print('Created By',getattr(host,'createdBy'))
        host.update(oldValues,currentUser)
        print('after update',host.address.state,host.status)
        hostResponse = AdminHostResponse(host)
        response = hostResponse.data
        status = HTTP_200_OK
      else:
        print("Host Data invalid")
        response, status = hostRequest.errors, HTTP_400_BAD_REQUEST
    except Host.DoesNotExist:
        response, status = dict(error = "Host not found"), HTTP_404_NOT_FOUND
    except Host.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Hosts found"), HTTP_400_BAD_REQUEST

    return response, status   

  @classmethod
  def deleteHost(cls,id,currentUser):
    try:
      host = Host.objects.get(id=id)
      host.delete(currentUser=currentUser)
      response = dict(message = "Host Deleted")
      status = HTTP_200_OK
    except Host.DoesNotExist:
        response, status = dict(error = "Host not found"), HTTP_404_NOT_FOUND

    except Host.MultipleObjectsReturned:
        response, status = dict(error = "Multiple Hosts found"), HTTP_400_BAD_REQUEST
        print("Multiple Hosts with one id, WTF!!")

    return response, status