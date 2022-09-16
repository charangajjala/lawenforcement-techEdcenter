from hosts.models import Host
from classes.models import Roster,Class
from classes.serializers import HostResponse

from rest_framework.status import *

from datetime import datetime

class HostDashboardServices:
  @classmethod
  def currentClasses(cls,user):
    try:
      hostObj = Host.objects.get(contactUser=user)
      classObjs = Class.objects.filter(host=hostObj)
      currentClasses=[]
      for classObj in classObjs:
        today = datetime.now()
        endDate = getattr(classObj,'endDate')
        endTime = getattr(classObj,'endTime')
        day =datetime.combine(endDate,endTime)
        if day>=today:
          currentClasses.append(classObj)
      classes = HostResponse(currentClasses,many=True)
      response,status = classes.data,HTTP_200_OK
    except Host.DoesNotExist:
      response,status = dict('This user is not a host'),HTTP_400_BAD_REQUEST
    except Host.MultipleObjectsReturned:
      response,status = dict('There are multiple hosts to same user'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def pastClasses(cls,user):
    try:
      hostObj = Host.objects.get(contactUser=user)
      classObjs = Class.objects.filter(host=hostObj)
      pastClasses=[]
      for classObj in classObjs:
        today = datetime.now()
        endDate = getattr(classObj,'endDate')
        endTime = getattr(classObj,'endTime')
        day =datetime.combine(endDate,endTime)
        if day<today:
          pastClasses.append(classObj)
      classes = HostResponse(pastClasses,many=True)
      response,status = classes.data,HTTP_200_OK
    except Host.DoesNotExist:
      response,status = dict('This user is not a host'),HTTP_400_BAD_REQUEST
    except Host.MultipleObjectsReturned:
      response,status = dict('There are multiple hosts to same user'),HTTP_400_BAD_REQUEST
    return response,status