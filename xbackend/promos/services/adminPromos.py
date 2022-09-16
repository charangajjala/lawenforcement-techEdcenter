from typing import final
from django.http import response
from promos.serializers import AdminPromoRequest,AdminPromoResponse
from promos.models import Promo

from rest_framework.status import *

class AdminPromoServices:
  
  @classmethod
  def get(cls,id):
    promoObj = Promo.objects.get(id=id)
    promoResponse = AdminPromoResponse(promoObj)
    response,status = promoResponse.data,HTTP_200_OK
    return response,status

  @classmethod
  def update(cls,data,user,id):
    promoRequest = AdminPromoRequest(data=data,partial=True)
    if promoRequest.is_valid():
      validData = promoRequest.validated_data
      promoObj = Promo.objects.get(id=id)
      oldValues = {}
      for k,v in validData.items():
        oldValues[k] = getattr(promoObj,k)
        setattr(promoObj,k,v)
      promoObj.update(oldValues,user)
      promoResponse = AdminPromoResponse(promoObj)
      response,status = promoResponse.data,HTTP_200_OK
    else:
      print(promoRequest.errors)
      response,status = dict(error = 'promo update request is invalid'),HTTP_400_BAD_REQUEST
    return response,status

  @classmethod
  def delete(cls,user,id):
    try:
      promoObj = Promo.objects.get(id=id)
      promoObj.delete(currentUser = user)
      response,status = dict(message='Promo object deleted'),HTTP_200_OK
    except Promo.DoesNotExist:
      response,status = dict(message='Promo IS not found'),HTTP_400_BAD_REQUEST
    finally:
      return response,status

class AdminPromosServices:
  
  @classmethod
  def create(cls,data,user):
    promoRequest = AdminPromoRequest(data=data)
    if promoRequest.is_valid():
      validData = promoRequest.validated_data
      promoObj = Promo.objects.create(
        **dict(
          validData,
          createdBy = user
        )
      )
      promoResponse = AdminPromoResponse(promoObj)
      response,status = promoResponse.data, HTTP_200_OK
    else:
      print(promoRequest.errors)
      response,status =dict(error='Not a valid Request'),HTTP_400_BAD_REQUEST
    return response,status      

  @classmethod
  def get(cls,params):
    options = True if params.get('options') == 'true' else  False if params.get('options') == 'false' else None
    promoObjs = Promo.objects.all().order_by('id')
    if options==True:
      promoObjs = promoObjs.filter(isActive=True)
    promoResponse = AdminPromoResponse(promoObjs,many=True)
    response,status = promoResponse.data,HTTP_200_OK
    return response,status