from functools import partial
from .serializers import HoursRequest
from .models import Hours

from django.db.models.query_utils import Q

from rest_framework.status import *

import datetime
import calendar

class AdminHoursServices:

  @classmethod
  def create(cls,data,user):
    hoursRequest = HoursRequest(data=data)
    if hoursRequest.is_valid():
      validData = hoursRequest.validated_data
      hours = validData.pop('hours')
      if hours >24:
        response,status = dict(message='Hours must not exceed 24'),HTTP_400_BAD_REQUEST
        return response,status
      else:
        Hours.objects.create(
          **dict(
            validData,
            hours = hours,
            createdBy=user,
          )
        )
      response,status = dict(message='Your Holiday equest has been created'),HTTP_200_OK
    else:
      print('Data Invalid',hoursRequest.errors)
      response,status = dict(error='Hours Request is not a valid one'),HTTP_400_BAD_REQUEST
    return response,status
  
  @classmethod
  def update(cls,data,user):
    hoursRequest = HoursRequest(data=data,partial=True)
    if hoursRequest.is_valid():
      validData = hoursRequest.validated_data
      nonFormatedDate = validData.pop('date',None)
      if nonFormatedDate == None:
        response,status = dict(errro='we need a Date'),HTTP_400_BAD_REQUEST
        return response,status
      date = datetime.datetime.strftime(nonFormatedDate,"%Y-%m-%d")
      hourObj = Hours.objects.get(date=date)
      oldValues={}
      for k,v in validData.items():
        oldValues[k] = getattr(hourObj,k)
        setattr(hourObj,k,v)
      oldValues['date']=date
      setattr(hourObj,'date',date)
      hourObj.update(oldValues,currentUser=user)
      response,status = dict(message='Your Holiday equest has been created'),HTTP_200_OK
    else:
      print('Data Invalid')
      response,status = dict(error='Hours Request is not a valid one'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def get(cls,query_params):
    month = query_params.get('month')
    year = query_params.get('year')
    if month == None or year == None:
      monthNumber = datetime.datetime.now().month
      year = datetime.datetime.now().year
      month = calendar.month_abbr[monthNumber]
    month_tonumber = {name:num for num,name in enumerate(calendar.month_abbr) if name}
    monthNumber = month_tonumber[month]
    hourObj = Hours.objects.filter(date__year=year,date__month=monthNumber)
    hoursResponse = HoursRequest(hourObj,many=True)
    response,status = hoursResponse.data,HTTP_200_OK
    return response,status